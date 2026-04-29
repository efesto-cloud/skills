# Clarification Rules

## Principle

Ask the user only when the extraction data is genuinely ambiguous.
**Never ask what can be inferred.** Prefer one good question over three vague ones.
Maximum 3 questions per session. After the user answers, do not ask again.

---

## Decision Tree

Work through these checks in order. Stop as soon as you have enough context.

### Check 1 — Unknown sheet roles

IF 2 or more sheets have role = `unknown`:

Ask: *"Ho trovato [N] fogli il cui scopo non è chiaro dai nomi e dai dati.
Puoi descrivere brevemente a cosa servono questi fogli?"*

List the unknown sheets with their dimensions as context clues.

Skip if: all unknown sheets are clearly empty or are cover/notes sheets by visual inspection.

---

### Check 2 — Generic sheet names

IF more than half the sheets are named Sheet1, Sheet2, Foglio1, Tab_X, etc.:

Ask: *"I fogli hanno nomi generici. Puoi dirmi a cosa corrispondono?
Anche solo una parola per foglio va bene — es. 'Sheet1 = dati di input filiali'."*

Provide the list as a fill-in prompt to make it easy.

Skip if: workbook_type = data_table (generic names are common and less important).

---

### Check 3 — Ambiguous consolidation structure

IF workbook_type = consolidation AND any of:
- Cannot identify which sheet is the consolidated total
- Cannot identify which sheets are entities vs. calculations
- Elimination/intercompany sheet is absent but expected

Ask: *"Sembra un file di consolidamento. Puoi confermare:
(a) qual è il foglio del consolidato finale?
(b) i fogli con nomi di società rappresentano ciascuno un'entità separata?
(c) c'è un foglio di eliminazioni infragruppo?"*

---

### Check 4 — Ambiguous time dimension

IF workbook_type = financial_model or budget_forecast AND:
- Cannot determine if columns = months, quarters, or years
- Header row values are numbers (1, 2, 3…) without labels

Ask: *"Le colonne numeriche rappresentano mesi, trimestri o anni?"*

---

### Check 5 — External links

IF external links are detected:

Ask: *"Il file contiene riferimenti a file Excel esterni. Vuoi caricare anche quei file
per mappare le relazioni complete, o posso procedere considerando solo questo file?"*

---

## What NOT to Ask

Never ask:
- "Che tipo di file è questo?" — infer from data
- "Quanti fogli ha?" — already known
- "Stai usando formule?" — already detected
- "Qual è lo scopo generale del file?" — infer from classification
- Anything answerable from the extracted JSON data

---

## Formatting Questions

Keep questions short and concrete. Use Italian when the file content is in Italian.
Provide context (sheet names, dimensions) alongside each question to help the user answer quickly.
Group multiple sub-questions into one ask where possible.
