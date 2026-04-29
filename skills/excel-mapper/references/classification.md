# Classification Rules

## Workbook Type Detection

Examine sheet names, column headers, and formula patterns to classify the workbook.
Use the FIRST matching rule.

### financial_model
Triggers if ANY of:
- Sheet names contain: P&L, CE, SP, CF, BS, Income, Revenue, EBITDA, Stato Patrimoniale,
  Conto Economico, Cash Flow, Rendiconto, Margine, Budget, Forecast, Actual, Variance
- Columns contain: year headers (2020, 2021… or FY20, FY21…), month headers (Jan, Feb… Gen, Feb…)
- Formulas contain: SUM across year columns, SUMIF with period filters, NPV, IRR, XIRR

### consolidation
Triggers if ANY of:
- Sheet names contain: entity names, company abbreviations, "Group", "Consolidato",
  "Eliminazioni", "Elim", "Intercompany", "IC", "Holding", subsidiary-like names
- Multiple sheets share identical column structure (same headers, same row count)
- Formulas sum across sheets: =SUM(Sheet1:Sheet10!B5)

### budget_forecast
Triggers if ANY of:
- Sheet names contain: Budget, Forecast, Plan, Actual, Variance, Delta, Scostamento,
  Consuntivo, Preventivo, Rolling, Revised
- Columns alternate Actual/Budget/Variance patterns
- Named ranges contain "budget" or "forecast"

### report
Triggers if ANY of:
- Most sheets have no formulas (data-only or pivot-like)
- Sheet names contain: Report, Summary, Riepilogo, Sintesi, Dashboard, KPI, Overview
- Few source sheets, mostly output/formatted sheets

### data_table
Triggers if:
- File has 1–3 sheets
- Sheets are purely tabular (consistent headers row 1, data rows below, no section breaks)
- Few or no cross-sheet references

### mixed
Use when 2+ types apply with similar weight. Note the dominant type.

---

## Sheet Role Detection

Classify each non-empty sheet into one role. Use ALL matching signals.

### source
- Other sheets reference this sheet but it references no others
- Contains raw data (IDs, dates, text values, hardcoded numbers)
- Column headers are descriptive nouns (not formula results)
- Few or no formulas

### calculation
- References 1+ other sheets AND is referenced by 1+ other sheets
- High formula density (>30% of used cells are formulas)
- Contains intermediate calculations, subtotals, allocations

### output / dashboard
- Referenced by no other sheet (leaf node in dependency graph)
- High formatting density
- Contains charts, summary tables, management-ready layout
- Sheet names: Dashboard, Report, Output, Sintesi, Riepilogo, Summary

### lookup
- Contains reference tables used via VLOOKUP/XLOOKUP/INDEX-MATCH
- Usually small (< 500 rows), 2–5 columns
- Sheet names: Lookup, Tables, Ref, Parametri, Liste, Codici, Mappings

### notes / documentation
- Very few formulas
- Mostly text, long strings, comments
- Sheet names: Note, Legenda, Instructions, Istruzioni, ReadMe, Cover

### unknown
- Cannot be classified with confidence
- Triggers a clarification question to the user

---

## Layout Pattern Detection

### tabular
- Row 1 (or first non-empty row) = headers
- All subsequent rows = data
- No merged cells spanning more than 1 row in the data area
- Consistent column count throughout

### block
- Multiple "tables" stacked vertically or side by side
- Section titles interspersed between data blocks
- Merged cells used for section headers
- Blank rows used as separators
- Typical of financial statements (SP, CE, CF)

### hybrid
- Tabular area + metadata block (e.g., top section has parameters, bottom has data table)
- Mixed merged and non-merged areas

---

## Complexity Scoring

Score each factor and sum:

| Factor | Points |
|--------|--------|
| > 10 non-empty sheets | +2 |
| > 25 non-empty sheets | +3 (replaces above) |
| Cross-sheet references in > 50% of sheets | +2 |
| Circular references detected | +2 |
| External links present | +1 |
| Named ranges > 10 | +1 |
| block or hybrid layout dominant | +1 |
| workbook_type = consolidation | +2 |
| Total formulas > 500 | +1 |

**Score 0–2 → simple | 3–5 → medium | 6+ → complex**
