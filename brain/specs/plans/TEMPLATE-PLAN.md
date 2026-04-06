# [Feature Name] - Implementation Plan

> **Status**: 🟡 In Progress  
> **Priority**: High | Medium | Low  
> **Started**: YYYY-MM-DD  
> **Target**: YYYY-MM-DD  
> **Completed**: -

---

## Goal

One or two sentences: what are we building and why?

**Problem**: What problem does this solve?

**Success Criteria**: How do we know we're done?
- [ ] Criterion 1
- [ ] Criterion 2

---

## Current State

What exists today:
- Entity X has properties A, B, C
- Use case Y does Z
- Missing: feature M

**Links**:
- Related spec: [EntityName](../entities/EntityName.md)
- Draft request: [../drafts/feature-requests.md](../drafts/feature-requests.md#feature-name)

---

## Target State

What we want:
- New entity X with properties D, E, F
- New use cases: Create, Update, List
- Admin route for management
- Client route for usage

**Links**:
- Planned spec: [NewEntity](../entities/NewEntity.md) (create during implementation)

---

## Dependencies

What needs to exist first:
- [ ] Dependency 1 (link to plan or spec)
- [ ] Dependency 2

**Blockers**:
- None currently

---

## Implementation Phases

### Phase 1: Core Domain Layer
> **Goal**: Entity + basic persistence

- [ ] Create entity spec: `entities/EntityName.md`
- [ ] Define type unions (if needed)
- [ ] Implement entity class with factory
- [ ] Create DTO interface
- [ ] Create document type
- [ ] Create mapper (entity ↔ document, entity ↔ DTO)
- [ ] Create repository interface
- [ ] Implement repository
- [ ] Register in DI container
- [ ] Run typecheck

**Notes**: Any tricky logic or examples

---

### Phase 2: Use Cases
> **Goal**: Business operations

- [ ] Create use case specs: `usecases/CreateEntity.md`, `usecases/UpdateEntity.md`
- [ ] Implement CreateEntity use case
- [ ] Implement UpdateEntity use case
- [ ] Implement DeleteEntity use case
- [ ] Implement GetEntity use case
- [ ] Implement ListEntity use case
- [ ] Add audit decorators
- [ ] Register use cases in DI
- [ ] Run typecheck

---

### Phase 3: Admin Interface
> **Goal**: Admin routes + UI

- [ ] Create route structure: `/admin/entities`
- [ ] Implement list loader + view
- [ ] Implement detail loader + view
- [ ] Implement create action + form
- [ ] Implement update action + form
- [ ] Implement delete action + confirmation
- [ ] Add to admin navigation
- [ ] Test in browser
- [ ] Verify audit logs created

---

### Phase 4: Client Interface (if needed)
> **Goal**: Client-facing features

- [ ] Create client routes
- [ ] Implement loaders
- [ ] Implement views
- [ ] Test as client user

---

### Phase 5: Polish & Documentation
> **Goal**: Production-ready

- [ ] Add missing indexes to database
- [ ] Update `ARCHITECTURE.md`
- [ ] Update `entities/index.md`
- [ ] Update `usecases/index.md`
- [ ] Mark entity specs as ⚪ Implemented
- [ ] Mark use case specs as ⚪ Implemented
- [ ] Clean up drafts
- [ ] Mark this plan as ✅ Complete

---

## Technical Notes

### Tricky Logic

If there's complex business logic, sketch it here:

```typescript
// Example: State transition validation
if (currentState === "draft" && newState === "published") {
  // Only allow if all required fields are filled
  if (!entity.hasRequiredFields()) {
    return ValidationError.create("Cannot publish incomplete entity");
  }
}
```

### Database Considerations

- Index on `{ field1: 1, field2: 1 }` for performance
- Compound unique constraint on `{ name: 1, parent_id: 1 }`
- Text index for search

### Special Requirements

- Must handle race conditions on counter updates (use atomic increment)
- SVG processing requires specific library: `svgo` with config X

---

## Testing Strategy

How to verify this works:
1. Unit test entity factory methods
2. Integration test repository CRUD
3. Manual test use cases via admin UI
4. Verify audit trail in database

---

## Risks & Mitigations

**Risk**: Dependency X might not work  
**Mitigation**: Have fallback Y ready

---

## Progress Log

Track major milestones as you go:

- **2026-04-06**: Plan created, started Phase 1
- **2026-04-07**: Entity + DTO done, working on mapper
- **2026-04-10**: Phase 1 complete, starting use cases

---

## Related Plans

Link to other plans that interact with this:
- [other-plan.md](./other-plan.md) - Related feature
