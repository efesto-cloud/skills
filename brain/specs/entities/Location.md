# Location

> **Status**: ⚪ Implemented  
> **Collection**: `locations`  
> **Soft Delete**: No

Physical funeral service location. Each operator belongs to one location.

---

## Core Properties

```
_id, display_name, address{street, city, state, postal_code, country}, created_at
```

**Unique**: `display_name`

---

## Relationships

- Each Location has many [Operators](../Operator.md) (via `location_id` foreign key)

**Population**: Operators are NOT populated (too heavy for list views)

---

## Business Rules

- `display_name` must be unique across all locations
- Cannot delete a Location if it has any Operators (foreign key constraint)
- Hard delete only (no soft delete - foundational data)

---

## What You Can Do

See use cases:
- [CreateLocation](../usecases/CreateLocation.md) - Create new location (ADMIN)
- [UpdateLocation](../usecases/UpdateLocation.md) - Update name or address (ADMIN)
- [DeleteLocation](../usecases/DeleteLocation.md) - Hard delete (ADMIN, must have no operators)
- [GetLocation](../usecases/GetLocation.md) - Get by ID
- [ListLocations](../usecases/ListLocations.md) - List all locations

---

## Database

**Indexes**:
- `{ _id: 1 }` - Primary key
- `{ display_name: 1 }` - Unique constraint for validation

**No soft delete** - `deleted_at` field doesn't exist

---

## Admin Routes

```
GET  /admin/locations              → List view
GET  /admin/locations/new          → Create form
GET  /admin/locations/:id          → Detail/edit view
POST /api/locations                → Create action
PATCH /api/locations/:id           → Update action
DELETE /api/locations/:id          → Delete action
```

Not exposed in client webapp (admin-only).

---

## Audit Trail

- **CREATE**: "Nuova Location" with `display_name` in metadata
- **UPDATE**: "Modifica Location" with changed fields
- **DELETE**: "Elimina Location"

---

## Implementation

**Files**:
- Entity: `/src/entity/Location.ts`
- DTO: `/src/dto/ILocation.ts`
- Document: `/src/db/Documents/LocationDoc.ts`
- Mapper: `/src/mapper/LocationMapper.ts`
- Repo: `/src/repo/ILocationRepo.ts` + `/src/repo/impl/LocationRepoImpl.ts`
- Use cases: `/src/useCase/location/*`

**DI Symbols**:
- `Symbols.Repo.LocationRepo`
- `Symbols.UseCase.Location.*`

---

## Notes

- Simple foundational entity
- No complex business logic
- Future: Could add "inactive" flag if locations close but need historical data
