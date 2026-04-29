#!/usr/bin/env python3
"""
render_map.py — Excel Mapper v2 renderer
Takes extracted JSON + context JSON → produces multi-file Markdown map.

Usage:
    python render_map.py <workbook_data.json> <workbook_context.json> <output_dir/>
"""

import sys, os, json, re
from datetime import datetime


# ── validation ───────────────────────────────────────────────────────────────

VALID_WORKBOOK_TYPES = {
    "financial_model", "consolidation", "budget_forecast",
    "report", "data_table", "mixed", "unknown"
}
VALID_SHEET_ROLES = {
    "source", "calculation", "output", "dashboard",
    "lookup", "notes", "unknown"
}
VALID_LAYOUT_PATTERNS = {"tabular", "block", "hybrid"}

def validate_context(context: dict) -> list:
    """Validate workbook_context.json. Returns warning strings; sets safe defaults.
    Raises ValueError only if sheet_roles is the wrong type."""
    warnings = []

    if "workbook_type" not in context:
        warnings.append("Missing 'workbook_type'; defaulting to 'unknown'")
        context["workbook_type"] = "unknown"
    elif context["workbook_type"] not in VALID_WORKBOOK_TYPES:
        warnings.append(f"Unknown workbook_type: '{context['workbook_type']}'")

    if "sheet_roles" not in context:
        warnings.append("Missing 'sheet_roles'; all sheet roles will show as 'unknown'")
        context["sheet_roles"] = {}
    elif not isinstance(context["sheet_roles"], dict):
        raise ValueError("'sheet_roles' must be a JSON object")
    else:
        for sheet, role in context["sheet_roles"].items():
            if role not in VALID_SHEET_ROLES:
                warnings.append(f"Sheet '{sheet}' has unknown role '{role}'")

    if "layout_pattern" in context and context["layout_pattern"] not in VALID_LAYOUT_PATTERNS:
        warnings.append(f"Unknown layout_pattern: '{context['layout_pattern']}'")

    if "split_output" in context and not isinstance(context["split_output"], bool):
        warnings.append("'split_output' should be a boolean")

    if "user_clarifications" in context and not isinstance(context["user_clarifications"], dict):
        warnings.append("'user_clarifications' should be a JSON object")
        context["user_clarifications"] = {}

    return warnings


# ── helpers ──────────────────────────────────────────────────────────────────

def slug(name):
    s = re.sub(r'[^\w\-]', '_', name)
    return s[:40]

def role_emoji(role):
    return {
        "source":      "📥",
        "calculation": "⚙️",
        "output":      "📤",
        "dashboard":   "📊",
        "lookup":      "🔍",
        "notes":       "📝",
        "unknown":     "❓"
    }.get(role, "")

def complexity_score(data, context):
    score = 0
    non_empty = data["non_empty_sheets"]
    if non_empty > 10: score += 2
    if non_empty > 25: score += 1
    if data["total_formulas"] > 500: score += 1
    if data["has_external_links"]: score += 1
    if len(data["named_ranges"]) > 10: score += 1
    if context.get("workbook_type") == "consolidation": score += 2
    sheets_with_refs = sum(
        1 for s in data["sheets"]
        if not s.get("empty") and (s.get("outgoing_refs") or s.get("incoming_refs"))
    )
    if non_empty > 0 and sheets_with_refs / non_empty > 0.5: score += 2
    return score

def decide_split(data, context):
    score = complexity_score(data, context)
    non_empty = data["non_empty_sheets"]
    if score >= 6 or non_empty > 25:
        return "complex"
    elif score >= 3 or non_empty > 10:
        return "medium"
    else:
        return "simple"

def fmt_list(items, bullet="- "):
    return "\n".join(f"{bullet}`{i}`" for i in items) if items else "_none_"

def ascii_flow(data, context):
    roles = context.get("sheet_roles", {})
    sources = [s["name"] for s in data["sheets"] if not s.get("empty") and roles.get(s["name"]) == "source"]
    calcs   = [s["name"] for s in data["sheets"] if not s.get("empty") and roles.get(s["name"]) == "calculation"]
    outputs = [s["name"] for s in data["sheets"] if not s.get("empty") and roles.get(s["name"]) in ("output", "dashboard")]
    lookups = [s["name"] for s in data["sheets"] if not s.get("empty") and roles.get(s["name"]) == "lookup"]

    lines = ["```"]
    if sources:
        lines.append("INPUT (source)")
        for s in sources: lines.append(f"  [{s}]")
        lines.append("      │")
    if lookups:
        lines.append("LOOKUP")
        for s in lookups: lines.append(f"  [{s}]")
        lines.append("      │")
    if calcs:
        lines.append("CALCULATION")
        for s in calcs: lines.append(f"  [{s}]")
        lines.append("      │")
    if outputs:
        lines.append("OUTPUT")
        for s in outputs: lines.append(f"  [{s}]")
    if not (sources or calcs or outputs):
        lines.append("(sheet relationships not determined)")
    lines.append("```")
    return "\n".join(lines)

def interpret_formula(formula: str) -> str:
    """Return an English semantic description of an Excel formula."""
    f = formula.upper()
    parts = []

    # Lookups — most specific first
    if "XLOOKUP" in f:
        parts.append("table lookup (XLOOKUP)")
    elif "INDEX" in f and "MATCH" in f:
        parts.append("table lookup (INDEX/MATCH)")
    elif "VLOOKUP" in f:
        parts.append("vertical lookup")
    elif "HLOOKUP" in f:
        parts.append("horizontal lookup")

    # Aggregates
    if "SUMPRODUCT" in f:
        parts.append("weighted sum / array product")
    elif "SUMIFS" in f:
        parts.append("conditional sum (multi-criteria)")
    elif "SUMIF" in f:
        parts.append("conditional sum")
    elif re.search(r"\bSUM\(", f):
        parts.append("sum")

    if "AVERAGEIFS" in f:
        parts.append("conditional average (multi-criteria)")
    elif "AVERAGEIF" in f:
        parts.append("conditional average")
    elif "AVERAGE" in f:
        parts.append("average")

    if "COUNTIFS" in f:
        parts.append("conditional count (multi-criteria)")
    elif "COUNTIF" in f:
        parts.append("conditional count")
    elif re.search(r"\bCOUNTA?\(", f):
        parts.append("count")

    if "MAXIFS" in f:
        parts.append("conditional max")
    elif re.search(r"\bMAX\(", f):
        parts.append("max value")

    if "MINIFS" in f:
        parts.append("conditional min")
    elif re.search(r"\bMIN\(", f):
        parts.append("min value")

    # Financial
    if any(fn in f for fn in ("NPV", "IRR", "XIRR", "XNPV")):
        parts.append("financial calculation")
    if any(fn in f for fn in ("PMT(", "PPMT(", "IPMT(")):
        parts.append("loan/payment calculation")

    # Logic / error handling
    if "IFERROR" in f or "IFNA" in f:
        parts.append("error handling")
    if re.search(r"\bIFS\(", f):
        parts.append("multi-condition branch")
    elif re.search(r"\bIF\(", f):
        parts.append("conditional branch")

    # Dynamic references
    if "INDIRECT" in f:
        parts.append("indirect reference")
    if "OFFSET" in f:
        parts.append("dynamic range reference")

    # Text
    if any(fn in f for fn in ("CONCAT(", "CONCATENATE(", "TEXTJOIN(")):
        parts.append("text concatenation")

    # Date/time
    if any(fn in f for fn in ("EDATE", "EOMONTH", "NETWORKDAYS", "WORKDAY")):
        parts.append("date calculation")
    elif re.search(r"\bDATE\(", f):
        parts.append("date calculation")
    if any(fn in f for fn in ("TODAY(", "NOW(")):
        parts.append("current date/time")

    # Cross-sheet fallback
    if not parts and re.search(r"!\$?[A-Z]+\$?\d+", formula):
        parts.append("cross-sheet reference")

    return "; ".join(parts) if parts else ""


# ── renderers ────────────────────────────────────────────────────────────────

def render_index(data, context, split_mode, output_dir, sheet_files):
    roles = context.get("sheet_roles", {})
    wtype = context.get("workbook_type", "unknown")
    complexity = context.get("complexity", "?")
    filename = data["filename"]
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        f"# 📋 Excel Map — `{filename}`",
        f"> Generated {ts} · Type: **{wtype}** · Complexity: **{complexity}**\n",
        "---\n",
        "## 📁 Workbook Overview\n",
        "| Attribute | Value |",
        "|-----------|-------|",
        f"| Total sheets | {data['sheet_count']} |",
        f"| Non-empty sheets | {data['non_empty_sheets']} |",
        f"| Total formulas | {data['total_formulas']} |",
        f"| Named ranges | {len(data['named_ranges'])} |",
        f"| External links | {'⚠️ Yes' if data['has_external_links'] else 'No'} |",
        f"| Circular refs | {'⚠️ Yes' if data.get('has_circular_refs') else 'No'} |",
        f"| Output mode | {split_mode} |",
        "",
    ]

    clarifs = context.get("user_clarifications", {})
    if clarifs:
        lines += ["## 💬 User-Provided Context\n"]
        for sheet, note in clarifs.items():
            lines.append(f"- **{sheet}**: {note}")
        lines.append("")

    lines += ["---\n", "## 📑 Sheet Inventory\n"]

    if split_mode == "simple":
        lines += [
            "| N | Sheet | Role | Dimensions | Layout | Formulas | Referenced by | References |",
            "|---|-------|------|------------|--------|----------|---------------|------------|"
        ]
    else:
        lines += [
            "| N | Sheet | Role | Dimensions | Layout | Formulas | Detail |",
            "|---|-------|------|------------|--------|----------|--------|"
        ]

    for i, s in enumerate(data["sheets"], 1):
        name = s["name"]
        if s.get("empty"):
            if split_mode == "simple":
                lines.append(f"| {i} | {name} | — | _empty_ | — | — | — | — |")
            else:
                lines.append(f"| {i} | {name} | — | _empty_ | — | — | — |")
            continue

        role = roles.get(name, "unknown")
        emoji = role_emoji(role)
        dims = s.get("dimensions", "")
        layout = s.get("layout", "")
        fcount = s.get("formula_count", 0)
        inc = ", ".join(f"`{r}`" for r in s.get("incoming_refs", []))
        out = ", ".join(f"`{r}`" for r in s.get("outgoing_refs", []))

        if split_mode == "simple":
            lines.append(f"| {i} | **{name}** | {emoji} {role} | {dims} | {layout} | {fcount} | {inc or '—'} | {out or '—'} |")
        else:
            link_file = sheet_files.get(name, "")
            link = f"[→ detail]({link_file})" if link_file else ""
            lines.append(f"| {i} | **{name}** | {emoji} {role} | {dims} | {layout} | {fcount} | {link} |")

    lines.append("")

    lines += ["---\n", "## 🔄 Data Flow\n", ascii_flow(data, context), ""]

    non_empty = [s for s in data["sheets"] if not s.get("empty")]
    has_any_refs = any(s.get("outgoing_refs") or s.get("incoming_refs") for s in non_empty)
    if has_any_refs:
        lines += ["---\n", "## 🔗 Cross-Sheet Relationships\n"]
        for s in non_empty:
            name = s["name"]
            inc = s.get("incoming_refs", [])
            out = s.get("outgoing_refs", [])
            if inc or out:
                lines.append(f"**{name}**")
                if out: lines.append(f"  - Reads from: {', '.join(f'`{r}`' for r in out)}")
                if inc: lines.append(f"  - Read by: {', '.join(f'`{r}`' for r in inc)}")
        lines.append("")

    if data["named_ranges"]:
        lines += ["---\n", "## 🏷️ Named Ranges\n",
                  "| Name | Reference |",
                  "|------|-----------|"]
        for nr in data["named_ranges"]:
            lines.append(f"| `{nr['name']}` | `{nr['refers_to']}` |")
        lines.append("")

    anomalies = []
    circular = data.get("circular_refs", [])
    if circular:
        for c in circular:
            anomalies.append(f"⚠️ **Circular reference**: `{c}`")
    if data["has_external_links"]:
        anomalies.append("⚠️ **External links detected** — linked values may be stale without the source files")
    empty_sheets = [s["name"] for s in data["sheets"] if s.get("empty")]
    if empty_sheets:
        anomalies.append(f"ℹ️ **Empty sheets**: {', '.join(empty_sheets)}")
    unknowns = [s["name"] for s in non_empty if roles.get(s["name"]) == "unknown"]
    if unknowns:
        anomalies.append(f"❓ **Role undetermined**: {', '.join(unknowns)}")

    if anomalies:
        lines += ["---\n", "## ⚠️ Anomalies and Notes\n"]
        for a in anomalies: lines.append(a)
        lines.append("")

    if split_mode != "simple":
        lines += ["---\n", "## 📂 Map Files\n"]
        lines.append("- [`00_INDEX.md`](00_INDEX.md) — this file")
        for name, fname in sheet_files.items():
            lines.append(f"- [`{fname}`]({fname}) — sheet `{name}`")
        if context.get("complexity") == "complex":
            lines.append("- [`relationships.md`](relationships.md) — detailed relationships graph")
        lines.append("")

    lines.append("_Excel Mapper v2 — excel-mapper skill_")
    return "\n".join(lines)


def render_sheet(sheet_data, context, index):
    roles = context.get("sheet_roles", {})
    name  = sheet_data["name"]
    role  = roles.get(name, "unknown")
    clarif = context.get("user_clarifications", {}).get(name, "")

    lines = [
        f"# Sheet {index}: `{name}`",
        f"> Role: **{role_emoji(role)} {role}**"
        + (f" — {clarif}" if clarif else ""),
        ""
    ]

    lines += [
        "## Overview\n",
        "| Attribute | Value |",
        "|-----------|-------|",
        f"| Dimensions | {sheet_data.get('dimensions','')} |",
        f"| Used range | `{sheet_data.get('range','')}` |",
        f"| Layout | {sheet_data.get('layout','')} |",
        f"| Formulas | {sheet_data.get('formula_count',0)} ({sheet_data.get('formula_density',0)*100:.1f}% of cells) |",
        f"| External links | {'⚠️ Yes' if sheet_data.get('has_external_links') else 'No'} |",
        ""
    ]

    inc = sheet_data.get("incoming_refs", [])
    out = sheet_data.get("outgoing_refs", [])
    if inc or out:
        lines += ["## Cross-Sheet Relationships\n"]
        if out: lines.append(f"**Reads from:** {', '.join(f'`{r}`' for r in out)}")
        if inc: lines.append(f"**Read by:** {', '.join(f'`{r}`' for r in inc)}")
        lines.append("")

    cols = sheet_data.get("columns", [])
    if cols:
        lines += ["## Columns\n",
                  "| Col | Header | Data Type | Sample Values |",
                  "|-----|--------|-----------|---------------|"]
        for c in cols:
            samples = ", ".join(c.get("samples", [])) or "—"
            lines.append(f"| {c['letter']} | {c['header']} | {c['dtype']} | {samples} |")
        lines.append("")

    formulas = sheet_data.get("formulas", [])
    if formulas:
        lines += ["## Formulas\n",
                  "| Cell | Formula | Interpretation |",
                  "|------|---------|----------------|"]
        for fm in formulas[:30]:
            interp = interpret_formula(fm["formula"])
            f_trunc = fm["formula"][:80] + ("…" if len(fm["formula"]) > 80 else "")
            lines.append(f"| {fm['cell']} | `{f_trunc}` | {interp} |")
        if len(formulas) > 30:
            lines.append(f"| … | _+{len(formulas)-30} more formulas not shown_ | |")
        lines.append("")

    lines.append("[← Back to index](00_INDEX.md)\n")
    lines.append("_Excel Mapper v2_")
    return "\n".join(lines)


def render_relationships(data, context):
    roles = context.get("sheet_roles", {})
    non_empty = [s for s in data["sheets"] if not s.get("empty")]

    lines = [
        f"# Relationships — `{data['filename']}`\n",
        "## Dependency Graph\n",
        ascii_flow(data, context),
        "",
        "## Detailed Dependency Chains\n"
    ]

    for s in non_empty:
        name = s["name"]
        inc  = s.get("incoming_refs", [])
        out  = s.get("outgoing_refs", [])
        if not inc and not out: continue
        role = roles.get(name, "unknown")
        lines.append(f"### `{name}` ({role})\n")
        if out:
            lines.append("**Depends on:**")
            for r in out:
                r_role = roles.get(r, "unknown")
                lines.append(f"- `{r}` ({r_role})")
        if inc:
            lines.append("**Used by:**")
            for r in inc:
                r_role = roles.get(r, "unknown")
                lines.append(f"- `{r}` ({r_role})")
        lines.append("")

    circular = data.get("circular_refs", [])
    if circular:
        lines += ["## ⚠️ Circular References\n"]
        for c in circular:
            lines.append(f"- `{c}`")
        lines.append("")

    if data["has_external_links"]:
        lines += [
            "## ⚠️ External Links\n",
            "This workbook contains references to external Excel files.",
            "Sheets with external links:\n",
            "| Sheet | External link |",
            "|-------|---------------|"
        ]
        for s in non_empty:
            if s.get("has_external_links"):
                lines.append(f"| `{s['name']}` | ⚠️ Yes |")
        lines.append("")

    lines.append("[← Back to index](00_INDEX.md)\n_Excel Mapper v2_")
    return "\n".join(lines)


# ── main ─────────────────────────────────────────────────────────────────────

def render(data_path, context_path, output_dir):
    with open(data_path, encoding="utf-8") as f:
        data = json.load(f)
    with open(context_path, encoding="utf-8") as f:
        context = json.load(f)

    validation_warnings = validate_context(context)
    for w in validation_warnings:
        print(f"  ⚠️  Context warning: {w}")

    os.makedirs(output_dir, exist_ok=True)

    split_mode = decide_split(data, context)
    context["complexity"] = split_mode

    non_empty = [s for s in data["sheets"] if not s.get("empty")]
    generated = []

    sheet_files = {}
    if split_mode in ("medium", "complex"):
        for i, s in enumerate(non_empty, 1):
            fname = f"sheet_{i:02d}_{slug(s['name'])}.md"
            fpath = os.path.join(output_dir, fname)
            content = render_sheet(s, context, i)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(content)
            sheet_files[s["name"]] = fname
            generated.append(fpath)
            print(f"  ✅ {fname}")

    if split_mode == "complex":
        rel_path = os.path.join(output_dir, "relationships.md")
        with open(rel_path, "w", encoding="utf-8") as f:
            f.write(render_relationships(data, context))
        generated.append(rel_path)
        print("  ✅ relationships.md")

    idx_path = os.path.join(output_dir, "00_INDEX.md")
    content = render_index(data, context, split_mode, output_dir, sheet_files)
    with open(idx_path, "w", encoding="utf-8") as f:
        f.write(content)
    generated.insert(0, idx_path)
    print("  ✅ 00_INDEX.md")

    print(f"\n✅ Map rendered ({split_mode} mode) → {len(generated)} files in {output_dir}")
    return generated


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: render_map.py <data.json> <context.json> <output_dir/>")
        sys.exit(1)
    render(sys.argv[1], sys.argv[2], sys.argv[3])
