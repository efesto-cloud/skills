#!/usr/bin/env python3
"""
plan_status.py — Dashboard view of all active implementation plans.

Usage:
    python scripts/plan_status.py               # show all plans grouped by status
    python scripts/plan_status.py --tree        # show as folder tree with status
    python scripts/plan_status.py --blocked     # show only blocked plans + their blockers
    python scripts/plan_status.py --progress    # show task completion % per plan

Exit code 0 always (read-only tool).
"""

import sys
import os
import re
import argparse
from pathlib import Path
from datetime import date, datetime

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. Run: pip install pyyaml")
    sys.exit(1)

# ── Parsing ──────────────────────────────────────────────────────────────────

def parse_plan(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    fm_text = text[3:end].strip()
    body = text[end + 4:]
    try:
        fm = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError:
        return None

    # Count tasks
    total = len(re.findall(r'^\s*- \[[ x]\]', body, re.MULTILINE))
    done  = len(re.findall(r'^\s*- \[x\]',   body, re.MULTILINE))

    return {
        "path":       path,
        "scope":      fm.get("scope", "?"),
        "status":     fm.get("status", "?"),
        "spec":       fm.get("spec"),
        "blocked_by": fm.get("blocked-by"),
        "unblocks":   fm.get("unblocks"),
        "updated":    fm.get("updated"),
        "tasks_total": total,
        "tasks_done":  done,
    }

def find_all_plans() -> list[dict]:
    plans = []
    for p in sorted(Path(".").glob("todo/**/plan.md")):
        parsed = parse_plan(p)
        if parsed:
            plans.append(parsed)
    return plans

# ── Formatting helpers ────────────────────────────────────────────────────────

STATUS_ICON = {
    "not-started": "🔲",
    "in-progress":  "🔄",
    "blocked":      "🚫",
    "done":         "✅",
    "?":            "❓",
}

SCOPE_ICON = {
    "use-case": "⚙️ ",
    "entity":   "📦",
    "module":   "📂",
    "project":  "🗂️ ",
    "?":        "  ",
}

def progress_bar(done: int, total: int, width: int = 20) -> str:
    if total == 0:
        return f"{'─' * width} no tasks"
    pct = done / total
    filled = round(pct * width)
    bar = "█" * filled + "░" * (width - filled)
    return f"{bar} {done}/{total} ({pct:.0%})"

def staleness(updated) -> str:
    if not updated:
        return ""
    try:
        if isinstance(updated, str):
            d = datetime.strptime(updated, "%Y-%m-%d").date()
        else:
            d = updated
        delta = (date.today() - d).days
        if delta > 14:
            return f" ⚠️  last updated {delta}d ago"
        return f" (updated {delta}d ago)"
    except (ValueError, TypeError):
        return ""

# ── Views ─────────────────────────────────────────────────────────────────────

def view_grouped(plans: list[dict]):
    groups = {}
    for p in plans:
        groups.setdefault(p["status"], []).append(p)

    order = ["in-progress", "blocked", "not-started", "done", "?"]
    printed = False

    for status in order:
        if status not in groups:
            continue
        icon = STATUS_ICON.get(status, "")
        print(f"\n{icon}  {status.upper()}")
        print("─" * 50)
        for p in groups[status]:
            scope_icon = SCOPE_ICON.get(p["scope"], "  ")
            stale = staleness(p["updated"])
            print(f"  {scope_icon} {p['path']}{stale}")
            if p["blocked_by"]:
                print(f"       blocked by → {p['blocked_by']}")
        printed = True

    if not printed:
        print("No plans found under todo/")

def view_tree(plans: list[dict]):
    print("\n📁 todo/")
    by_path = {p["path"]: p for p in plans}
    for path in sorted(by_path.keys()):
        plan = by_path[path]
        depth = len(path.parts) - 1
        indent = "  " * depth
        icon = STATUS_ICON.get(plan["status"], "❓")
        scope = SCOPE_ICON.get(plan["scope"], "")
        print(f"{indent}{icon} {scope} {path.name}  [{'/'.join(path.parts[1:-1])}]")

def view_blocked(plans: list[dict]):
    blocked = [p for p in plans if p["status"] == "blocked"]
    if not blocked:
        print("✅  No blocked plans.")
        return
    print(f"\n🚫  {len(blocked)} blocked plan(s):\n")
    for p in blocked:
        print(f"  {p['path']}")
        if p["blocked_by"]:
            items = p["blocked_by"] if isinstance(p["blocked_by"], list) else [p["blocked_by"]]
            for item in items:
                blocker_path = Path(item)
                blocker_status = "?"
                if blocker_path.exists():
                    b = parse_plan(blocker_path)
                    if b:
                        blocker_status = b["status"]
                icon = STATUS_ICON.get(blocker_status, "❓")
                print(f"    └─ {icon} {item}  [{blocker_status}]")
        print()

def view_progress(plans: list[dict]):
    print(f"\n{'Plan':<55} {'Progress'}")
    print("─" * 90)
    for p in plans:
        label = str(p["path"])
        if len(label) > 54:
            label = "…" + label[-53:]
        bar = progress_bar(p["tasks_done"], p["tasks_total"])
        status_icon = STATUS_ICON.get(p["status"], "❓")
        print(f"{status_icon} {label:<53} {bar}")

    total_tasks = sum(p["tasks_total"] for p in plans)
    total_done  = sum(p["tasks_done"]  for p in plans)
    print("─" * 90)
    print(f"  {'TOTAL':<53} {progress_bar(total_done, total_tasks)}")

# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Show implementation plan status dashboard")
    parser.add_argument("--tree",     action="store_true", help="Show as folder tree")
    parser.add_argument("--blocked",  action="store_true", help="Show only blocked plans")
    parser.add_argument("--progress", action="store_true", help="Show task completion progress")
    args = parser.parse_args()

    plans = find_all_plans()

    if not plans:
        print("No plan.md files found under todo/")
        sys.exit(0)

    if args.tree:
        view_tree(plans)
    elif args.blocked:
        view_blocked(plans)
    elif args.progress:
        view_progress(plans)
    else:
        view_grouped(plans)
        print()

if __name__ == "__main__":
    main()
