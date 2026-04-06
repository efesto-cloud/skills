# [Feature Name] - Blueprint

> **Status**: 🔵 Draft  
> **Domain**: [Catalogo/Provino/Impresa/etc.]

## What & Why

Brief description of what this feature does and the problem it solves.

---

## Entity: EntityName

**Collection**: `entity_names` | **Soft Delete**: Yes/No

### Core Properties

```
_id, name, description, state, parent_id?, created_at, deleted_at?
```

### Type Unions

`TEntityState = "draft" | "active" | "archived"`

### Relationships

- Each EntityName belongs to a ParentEntity (via `parent_id`)
- Each EntityName has many ChildEntities
- EntityName references OtherEntity (FK only, not populated)

### Business Rules

- Name must be unique within parent scope
- Cannot delete if has active children
- State transitions: draft → active → archived (one-way)

---

## What You Can Do

### Create EntityName

As an **operator (ADMIN)**, I want to create a new entity with a name and optional parent. The name must be unique within the parent scope.

**Input**: `name`, `parent_id?`  
**Returns**: The created entity with generated ID

**Errors**:
- NotLoggedError - Invalid session
- PermissionError - Not ADMIN role
- DuplicateNameError - Name already exists for this parent
- NotFoundError - Parent doesn't exist

---

### Update EntityName

As an **operator (ADMIN)**, I want to update an entity's name or description. If the name changes, it must still be unique within the parent scope.

**Input**: `entity_id`, `name?`, `description?`  
**Returns**: The updated entity

**Errors**:
- NotLoggedError
- PermissionError
- NotFoundError - Entity doesn't exist
- DuplicateNameError - New name conflicts

---

### Delete EntityName

As an **operator (ADMIN)**, I want to soft-delete an entity. This sets `deleted_at` to the current time. Cannot delete if the entity has active (non-deleted) children.

**Input**: `entity_id`  
**Returns**: void (success)

**Errors**:
- NotLoggedError
- PermissionError
- NotFoundError
- CannotDeleteError - Has active children

---

### List EntityNames

As an **operator**, I want to retrieve a paginated list of entities. By default, deleted entities are excluded unless I specify `include_deleted: true`. I can filter by parent.

**Input**: `page?`, `limit?`, `parent_id?`, `include_deleted?`  
**Returns**: Page of entities with total count

**Errors**:
- NotLoggedError

---

### Search EntityNames

As an **operator**, I want to search entities by name using fuzzy search. Results are paginated and sorted by relevance.

**Input**: `q` (search query), `page?`, `limit?`  
**Returns**: Page of matching entities

**Errors**:
- NotLoggedError

---

## Repository Interface

```typescript
interface IEntityNameRepo {
  create(ctx, entity): Promise<Result<void, Error>>
  findById(ctx, id): Promise<Maybe<Entity>>
  update(ctx, entity): Promise<Result<void, Error>>
  softDelete(ctx, id): Promise<Result<void, Error>>
  list(ctx, filters, pagination): Promise<Result<Page<Entity>, Error>>
  search(ctx, query, pagination): Promise<Result<Page<Entity>, Error>>
  existsByName(ctx, name, parent_id): Promise<boolean>
}
```

---

## Database

**Indexes**:
- `{ _id: 1 }` - Primary
- `{ name: 1, parent_id: 1 }` - Unique constraint
- `{ parent_id: 1, deleted_at: 1 }` - List queries
- `{ name: "text" }` - Fuzzy search

---

## Admin Routes

```
GET  /admin/entities              → List view
GET  /admin/entities/new          → Create form
GET  /admin/entities/:id          → Detail/edit view
POST /api/entities                → Create action
PATCH /api/entities/:id           → Update action
DELETE /api/entities/:id          → Delete action
```

---

## Audit Trail

All mutations (Create, Update, Delete) are audited with:
- **CREATE**: "Nuovo EntityName"
- **UPDATE**: "Modifica EntityName"  
- **DELETE**: "Elimina EntityName"

---

## Implementation Order

1. Type union (if needed)
2. Entity class with factory method
3. DTO interface
4. Document type
5. Mapper (entity ↔ document, entity ↔ DTO)
6. Repository interface + implementation
7. DI symbols and bindings
8. Use case interfaces
9. Use case implementations + audit decorators
10. Admin routes (loader + action)
11. Typecheck + docs

---

## Open Questions

- [ ] Do we need a "restore" operation for soft-deleted entities?
- [ ] Should we track who deleted it?

---

## Notes

Any decisions, context, or gotchas worth remembering.
