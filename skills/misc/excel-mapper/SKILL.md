---
name: excel-mapper
description: >
  Use this skill IMMEDIATELY whenever a complex Excel file is uploaded and the user wants
  to analyze, edit, understand, query, or work with it in any non-trivial way. This skill
  generates a structured multi-file "map" of the workbook: a master index with hyperlinks
  plus one dedicated file per sheet, enabling progressive disclosure for large or complex files.
  It auto-detects structure (financial model, consolidation, budget, report, data table, mixed)
  and asks targeted clarifying questions only when the structure is ambiguous. Trigger proactively
  whenever: the file has more than 2 sheets, contains formulas or cross-sheet references, the user
  says Claude "gets confused" or "is slow", the user mentions bilancio, consolidato, budget,
  forecast, P&L, or any financial/complex workbook.
---

# Excel Mapper — v2

```
1. EXTRACT    → scripts/extract_map.py   (raw JSON)
2. CLASSIFY   → auto-detect type + sheet roles
3. CLARIFY    → ask only when ambiguous (max 3 questions)
4. RENDER     → scripts/render_map.py   (Markdown files)
5. PRESENT    → give files + load index into context
```

## Step 1 — Extract

```bash
ls /mnt/user-data/uploads/
python scripts/extract_map.py "/mnt/user-data/uploads/<FILE>" "/tmp/workbook_data.json"
```

## Step 2 — Classify

Read `/tmp/workbook_data.json` + `references/classification.md`. Determine workbook type,
sheet roles, layout pattern, and complexity level (simple / medium / complex).

## Step 3 — Clarify (only if needed)

Read `references/clarification_rules.md`. Never ask what can be inferred. Ask only when:
sheet role is `unknown` for 2+ sheets, names are generic (Sheet1…), or type confidence is low.

## Step 4 — Render

Output mode depends on complexity: simple → single file, medium → index + per-sheet,
complex → index + per-sheet + relationships. See [REFERENCE.md](REFERENCE.md) for context schema.

```bash
python scripts/render_map.py "/tmp/workbook_data.json" "/tmp/workbook_context.json" "/mnt/user-data/outputs/"
```

## Step 5 — Present

```python
with open("/mnt/user-data/outputs/00_INDEX.md") as f: print(f.read())
```

Present all files with `present_files`. Tell the user the map is ready, `00_INDEX.md` is
the entry point. Ask what they'd like to do next. **Respond in the workbook's language.**
Always consult the map before touching the raw file — the map is authoritative.

## Error Handling

| Situation | Action |
|-----------|--------|
| Password-protected | Ask user to remove protection |
| `.xls` format | Ask user to save as `.xlsx` |
| File > 50MB | Add `--sample-only` to extract_map.py |
| External links | Flag in INDEX; values may be stale |
| All sheets generic names | Ask user to describe each sheet |

## References

- [references/classification.md](references/classification.md) — workbook type + sheet role rules
- [references/clarification_rules.md](references/clarification_rules.md) — when/what to ask
- [REFERENCE.md](REFERENCE.md) — output structure, context JSON schema, in-session usage guide
