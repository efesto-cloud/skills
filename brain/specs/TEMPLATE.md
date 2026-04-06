# [Feature Name] - Design Spec

> **Status**: 🔵 Draft | 🟡 In Review | 🟢 Approved | ⚪ Implemented  
> **Created**: YYYY-MM-DD  
> **Domain**: [e.g., Catalogo, Provino, Impresa]

## Overview

Brief description of what this feature does and why it's needed.

**Problem**: What problem does this solve?  
**Solution**: High-level approach to solving it.

---

## Domain Model

### Entity: [EntityName]

**Type**: Entity | Value Object | Aggregate Root

#### Properties

| Property | Type | Required | Description | Notes |
|----------|------|----------|-------------|-------|
| `_id` | ObjectId | ✅ | Unique identifier | Auto-generated |
| `name` | string | ✅ | Display name | Max 255 chars |
| `state` | `TEntityState` | ✅ | Current state | See type union below |
| `created_at` | DateTime | ✅ | Creation timestamp | Auto-set |
| `deleted_at` | DateTime? | ❌ | Soft delete timestamp | Null if active |

#### Type Unions

```typescript
// TEntityState = "draft" | "active" | "archived"
// Define all discriminated unions or enums needed
```

#### Soft Delete

- [ ] Yes - Uses `deleted_at` field
- [ ] No - Hard delete only

Reasoning: [why soft delete is needed or not]

#### Relationships

```
EntityName
  ├─ belongsTo: ParentEntity (1:1 or N:1)
  ├─ hasMany: ChildEntity (1:N)
  └─ references: OtherEntity (via ID only, no population)
```

**Relationship Details**:
- `parent_id`: Reference to ParentEntity - Required, indexed
- `children`: Array of ChildEntity IDs - Populated on request
- `other_entity_id`: Foreign key only - Not populated

#### Validation Rules

- Name must be unique within parent scope
- State transitions: draft → active → archived (no going back)
- Cannot delete if has active children
- [Any other business constraints]

---

## Use Cases

### 1. Create[EntityName]

**Description**: Creates a new entity instance.

**Actor**: Operator (requires role: ADMIN)

**Input**:
```typescript
{
  operator_session_id: string,
  name: string,
  parent_id?: string,
  // ... other creation fields
}
```

**Output**:
```typescript
Result<IEntityName, NotLoggedError | ValidationError | Error>
```

**Business Logic**:
1. Validate operator session
2. Check permissions (ADMIN role required)
3. Validate input (name uniqueness, parent exists)
4. Create entity with status = "draft"
5. Audit log: CREATE operation

**Errors**:
- `NotLoggedError` - Invalid session
- `ValidationError` - Invalid input
- `DuplicateNameError` - Name already exists

---

### 2. Update[EntityName]

**Description**: Updates an existing entity.

**Actor**: Operator (requires role: ADMIN)

**Input**:
```typescript
{
  operator_session_id: string,
  entity_id: string,
  name?: string,
  // ... updatable fields
}
```

**Output**:
```typescript
Result<IEntityName, NotLoggedError | NotFoundError | Error>
```

**Business Logic**:
1. Validate session and permissions
2. Find entity by ID
3. Validate changes (e.g., name uniqueness if changed)
4. Update entity
5. Audit log: UPDATE operation

---

### 3. SoftDelete[EntityName]

**Description**: Marks entity as deleted without removing it.

**Actor**: Operator (requires role: ADMIN)

**Input**:
```typescript
{
  operator_session_id: string,
  entity_id: string,
}
```

**Output**:
```typescript
Result<void, NotLoggedError | NotFoundError | Error>
```

**Business Logic**:
1. Validate session
2. Check if entity can be deleted (no active children)
3. Set `deleted_at` to current timestamp
4. Audit log: DELETE operation

---

### 4. List[EntityName]

**Description**: Retrieves paginated list of entities.

**Actor**: Operator

**Input**:
```typescript
{
  operator_session_id: string,
  page?: number,
  limit?: number,
  include_deleted?: boolean,
  filter?: {
    parent_id?: string,
    state?: TEntityState,
  }
}
```

**Output**:
```typescript
Result<Page<IEntityName>, NotLoggedError | Error>
```

**Business Logic**:
1. Validate session
2. Build query with filters
3. Apply pagination
4. Populate relationships if needed
5. Return paginated results

---

## Repository Interface

```typescript
interface IEntityNameRepo {
  create(ctx: ITransactionContext, entity: EntityName): Promise<Result<void, Error>>;
  
  findById(
    ctx: ITransactionContext, 
    id: string, 
    options?: { populate?: boolean }
  ): Promise<Maybe<EntityName>>;
  
  update(ctx: ITransactionContext, entity: EntityName): Promise<Result<void, Error>>;
  
  softDelete(ctx: ITransactionContext, id: string): Promise<Result<void, Error>>;
  
  search(
    ctx: ITransactionContext,
    filters: IEntityNameSearchFilters,
    options: IPaginationOptions
  ): Promise<Result<Page<EntityName>, Error>>;
}
```

---

## Database Schema

**Collection Name**: `entity_names`

**Document Structure**:
```typescript
{
  _id: ObjectId,
  name: string,
  state: "draft" | "active" | "archived",
  parent_id?: ObjectId,
  created_at: Date,
  updated_at: Date,
  deleted_at?: Date,
}
```

**Indexes**:
- `{ _id: 1 }` - Primary key
- `{ parent_id: 1, deleted_at: 1 }` - List by parent, filter deleted
- `{ name: 1, parent_id: 1 }` - Unique name within parent
- `{ deleted_at: 1 }` - Soft delete queries

---

## Integration Points

### Admin Webapp

**Routes**:
- `GET /admin/entity-names` - List view
- `GET /admin/entity-names/:id` - Detail view
- `GET /admin/entity-names/new` - Create form
- `POST /api/entity-names` - Create action
- `PATCH /api/entity-names/:id` - Update action
- `DELETE /api/entity-names/:id` - Soft delete action

**Loader Data**:
```typescript
// admin.entity-names._index.tsx
{
  entities: Page<IEntityName>,
  filters: IEntityNameFilters,
}

// admin.entity-names.$id.tsx
{
  entity: IEntityName,
  parent?: IParentEntity,
}
```

### Client Webapp

Not exposed to client webapp (admin-only feature).

---

## Audit Requirements

All mutations (CREATE, UPDATE, DELETE) must be audited with:
- Entity type: `EntityName`
- Entity ID: The entity's `_id`
- Verb: CREATE | UPDATE | DELETE
- Title (Italian): "Nuovo EntityName" | "Modifica EntityName" | "Elimina EntityName"
- Metadata: Any relevant context (old vs new values for updates)

---

## Testing Checklist

- [ ] Entity factory method creates valid instances
- [ ] Validation rejects invalid data
- [ ] Use cases handle all error cases
- [ ] Soft delete sets timestamp correctly
- [ ] List excludes soft-deleted by default
- [ ] Audit logs are created for all mutations
- [ ] Repository CRUD operations work
- [ ] Mapper converts entity ↔ document correctly
- [ ] Population resolves relationships
- [ ] DI bindings are registered

---

## Open Questions

- [ ] Should we allow restoring soft-deleted entities?
- [ ] Do we need versioning for this entity?
- [ ] Should state transitions be logged separately?

---

## Implementation Checklist

Follow this order:

- [ ] 1. Define type union in `/src/type/` (if needed)
- [ ] 2. Create entity in `/src/entity/EntityName.ts`
- [ ] 3. Create DTO interface in `/src/dto/IEntityName.ts`
- [ ] 4. Create document type in `/src/db/Documents/EntityNameDoc.ts`
- [ ] 5. Create entity mapper in `/src/mapper/EntityNameMapper.ts`
- [ ] 6. Create repo interface in `/src/repo/IEntityNameRepo.ts`
- [ ] 7. Create repo implementation in `/src/repo/impl/EntityNameRepoImpl.ts`
- [ ] 8. Add DI symbols in `/src/di/Symbols.ts`
- [ ] 9. Register bindings in `/src/di/container.ts`
- [ ] 10. Create use case interfaces in `/src/useCase/entity-name/`
- [ ] 11. Create use case implementations in `/src/useCase/entity-name/impl/`
- [ ] 12. Add audit decorators to use cases
- [ ] 13. Create admin routes and loaders
- [ ] 14. Run typecheck: `pnpm run typecheck -w packages/core`
- [ ] 15. Update entity documentation in `/packages/doc/content/entity/`

---

## Notes

Any additional context, decisions, or references.
