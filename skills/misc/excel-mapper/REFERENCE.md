# Excel Mapper — Reference

## Output File Structure

### Always generated

**`00_INDEX.md`** — Master index:
- Workbook overview (type, size, complexity)
- Sheet inventory table with role, dimensions, link to per-sheet file
- Cross-sheet relationship map (ASCII diagram for complex workbooks)
- Key findings and anomalies (broken refs, empty sheets, external links)
- Quick-reference: named ranges, key formulas, data entry points

### Per sheet (medium / complex mode)

**`sheet_<N>_<SheetName>.md`** — One file per non-empty sheet:
- Sheet role and purpose (auto-detected or user-confirmed)
- Dimensions and used range
- Column inventory: letter, header, data type, sample values
- Formula inventory: cell, formula, semantic interpretation
- Incoming / outgoing cross-sheet references
- Layout notes (tabular / block / hybrid)
- Sheet-level anomalies

### Complex mode only

**`relationships.md`** — Cross-workbook relationship graph:
- Data flow diagram (ASCII, source → calc → output)
- Dependency chain per output sheet
- Circular reference warnings
- External link inventory

---

## Context JSON Schema

`workbook_context.json` passed to `render_map.py`:

```json
{
  "workbook_type": "financial_model",
  "sheet_roles": {
    "Assumptions": "source",
    "P&L": "calculation",
    "Dashboard": "output"
  },
  "layout_pattern": "block",
  "complexity": "complex",
  "user_clarifications": {
    "Sheet1": "Input data from foreign branches",
    "Tab_X": "Intercompany elimination reconciliation sheet"
  },
  "split_output": true
}
```

`user_clarifications` values should be in the user's language.

Valid values:
- `workbook_type`: `financial_model` | `consolidation` | `budget_forecast` | `report` | `data_table` | `mixed`
- `sheet_roles`: `source` | `calculation` | `output` | `dashboard` | `lookup` | `notes` | `unknown`
- `layout_pattern`: `tabular` | `block` | `hybrid`
- `complexity`: `simple` | `medium` | `complex`

---

## In-Session Usage Guide

Once the map is generated, always consult it before touching the raw Excel file.

| Task | What to read |
|------|-------------|
| Edit a formula | `sheet_N_<name>.md` → Formulas section |
| Explain how X is calculated | `relationships.md` → dependency chain |
| Understand overall structure | `00_INDEX.md` |
| Add a column to a sheet | `sheet_N_<name>.md` → Columns + Layout |
| Find an error or anomaly | `00_INDEX.md` → Anomalies |
| Trace where a value comes from | `relationships.md` → dependency chain |

Never re-read the raw Excel file for structural questions — the map is authoritative.
