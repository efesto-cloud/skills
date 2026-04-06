# Modello System - Implementation Plan

> **Status**: 🟡 In Progress  
> **Priority**: High  
> **Started**: 2026-01-15  
> **Target**: 2026-05-01  
> **Completed**: -

---

## Goal

Build a template system where operators can create reusable provino templates (Modelli) with pre-positioned elements, then generate new provini from these templates.

**Problem**: Operators manually recreate similar provino layouts for the same cemetery/dimensions. Wasteful and error-prone.

**Success Criteria**:
- [x] Operators can create modelli with positioned elements
- [ ] Operators can generate provino from modello
- [ ] Provino creation wizard includes modello selection (first step)
- [ ] Duplicate modello functionality works

---

## Current State

**What exists**:
- Modello entity: `_id`, `nome`, `descrizione?`, `dimensioni`, `elementi[]` (ElementoModello)
- ElementoModello: similar structure to ElementoProvino (transform + properties)
- Basic CRUD use cases: Create, Update, Delete, Get, List
- Admin routes: `/admin/modelli` (list, detail, create, edit)

**What's missing**:
- Generate provino from modello use case
- Wizard integration (modello selection as first step in provino creation)
- Duplicate modello use case
- Population of elemento references in modello.elementi

**Links**:
- Entity spec: [../entities/Modello.md](../entities/Modello.md) (needs updating)
- Draft request: [../drafts/feature-requests.md](../drafts/feature-requests.md#modello-system)

---

## Target State

**Complete modello system**:
- Modello CRUD (✅ done)
- Generate provino from modello (copies elementi with transforms)
- Wizard: Step 0 = "Choose modello (optional)", Step 1 = "Basic info", Step 2 = "Elementi"
- Duplicate modello (clone with new name)
- Admin can manage modelli library
- Operators can select from modelli when creating provino

---

## Dependencies

- [x] Provino entity exists
- [x] ElementoProvino structure defined
- [ ] Admin wizard refactored to support multi-step flow (blocker for wizard integration)

**Blockers**:
- Wizard refactor not started yet (move to separate plan if needed)

---

## Implementation Phases

### Phase 1: Core Modello System ✅ COMPLETE
> **Goal**: Entity + persistence + basic CRUD

- [x] Create modello entity spec
- [x] Implement Modello entity
- [x] Create IModello DTO
- [x] Create ModeloDoc document type
- [x] Create ModeloMapper
- [x] Create IModeloRepo interface
- [x] Implement ModeloRepoImpl
- [x] Register in DI
- [x] CreateModello use case
- [x] UpdateModello use case
- [x] DeleteModello (soft)
- [x] GetModello use case
- [x] ListModelli use case
- [x] Admin routes + UI

**Status**: ✅ Complete as of 2026-02-01

---

### Phase 2: Generate Provino from Modello
> **Goal**: Convert modello → provino

- [ ] Create use case spec: `usecases/GenerateProvinoFromModello.md`
- [ ] Define input: `modello_id`, `nome`, `cognome`, `data_nascita`, `data_decesso`, `cimitero`, `impresa_id`
- [ ] Implement use case:
  - Fetch modello by ID
  - Create new Provino with basic info
  - Copy dimensioni from modello
  - Copy each ElementoModello → ElementoProvino (same transforms)
  - Save provino
- [ ] Add audit decorator (verb: "GENERATE", title: "Generazione Provino da Modello")
- [ ] Register in DI
- [ ] Add admin action: `POST /api/provini/from-modello`
- [ ] Add button in modelli detail view: "Genera Provino"
- [ ] Test: Select modello, fill basic info, provino created with all elements positioned
- [ ] Run typecheck

**Technical Notes**:

```typescript
// Copy transform logic
const elementoProvino = ElementoProvino.create({
  elemento_id: elementoModello.elemento_id,
  variante_id: elementoModello.variante_id,
  transform: { ...elementoModello.transform }, // Same transform
  properties: { ...elementoModello.properties }, // Copy text/image properties
  note: elementoModello.note,
});
```

---

### Phase 3: Wizard Integration
> **Goal**: Add modello selection to provino creation flow

**Depends on**: Wizard refactor (not started)

- [ ] Create plan for wizard refactor (separate feature)
- [ ] OR: Simple approach - Add "Crea da modello" button on provini list that redirects to modello selection
- [ ] Implement modello selection modal
- [ ] On modello selected, redirect to create provino form with `modello_id` param
- [ ] Pre-fill dimensioni from selected modello
- [ ] Show preview of modello elements
- [ ] Test workflow

**Decision needed**: Full wizard vs simple button approach?

---

### Phase 4: Duplicate Modello
> **Goal**: Clone existing modello

- [ ] Create use case spec: `usecases/DuplicateModello.md`
- [ ] Define input: `modello_id`, `new_nome`
- [ ] Implement use case:
  - Fetch source modello
  - Create new Modello with copied data
  - Copy all elementi with transforms
  - Set new nome
  - Save
- [ ] Add audit decorator (verb: "DUPLICATE")
- [ ] Register in DI
- [ ] Add action: `POST /api/modelli/:id/duplicate`
- [ ] Add button in modelli detail: "Duplica"
- [ ] Test duplication
- [ ] Run typecheck

---

### Phase 5: Polish & Documentation
> **Goal**: Production-ready

- [ ] Add index on `modelli`: `{ deleted_at: 1 }`
- [ ] Update `ARCHITECTURE.md` with complete Modello info
- [ ] Update entity spec: `entities/Modello.md` → mark ⚪ Implemented
- [ ] Create use case specs for new operations
- [ ] Update `usecases/index.md`
- [ ] Clean up draft notes
- [ ] Mark this plan ✅ Complete

---

## Technical Notes

### ElementoModello vs ElementoProvino

Same structure:
- `elemento_id` (FK to Elemento)
- `variante_id?` (FK to Variante)
- `transform` (x, y, width, height, rotation, z_index)
- `properties` (tipo-specific: text content, image settings)
- `note?`

When generating provino, copy ElementoModello → ElementoProvino 1:1.

### Database

Modello collection already has:
- Index on `{ _id: 1 }`
- Index on `{ deleted_at: 1 }`

No additional indexes needed for now.

---

## Testing Strategy

1. **Create modello** with 3-4 positioned elements (text, images)
2. **Generate provino** from modello → verify all elements copied with correct transforms
3. **Edit provino** elements → verify modello unchanged
4. **Duplicate modello** → verify independent copy
5. **Delete modello** → verify soft delete, still visible with `include_deleted`

---

## Progress Log

- **2026-01-15**: Plan created, Phase 1 started
- **2026-02-01**: Phase 1 complete (CRUD + admin routes)
- **2026-03-10**: Phase 2 started (generate provino from modello)
- **2026-04-06**: Reviewing plan structure, Phase 2 ~40% done

---

## Related Plans

- [provino-improvements.md](./provino-improvements.md) - Provino duplicate & other features
- **Future**: Wizard refactor (needs separate plan)
