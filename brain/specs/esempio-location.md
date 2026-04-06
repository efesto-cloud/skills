# Location - Design Spec

> **Status**: ⚪ Implemented (example reference)  
> **Created**: 2026-01-15  
> **Domain**: Location Management

## Overview

A **Location** represents a physical funeral home location where services are provided. Each operator manages one location.

**Problem**: Need to track multiple funeral home locations, each with their own address and display name.

**Solution**: Simple entity with name and address. One-to-many relationship with operators.

---

## Domain Model

### Entity: Location

**Type**: Entity (Aggregate Root)

#### Properties

| Property | Type | Required | Description | Notes |
|----------|------|----------|-------------|-------|
| `_id` | ObjectId | ✅ | Unique identifier | Auto-generated |
| `display_name` | string | ✅ | Human-readable name | "Sede Milano Centro" |
| `address` | IAddress | ✅ | Physical address | Value object |
| `created_at` | DateTime | ✅ | Creation timestamp | Auto-set |

#### Type Unions

None - no state enum needed for Location.

#### Soft Delete

- [ ] Yes
- [x] No - Hard delete only

Reasoning: Locations are foundational data. If deleted, all related operators would be orphaned. Better to prevent deletion if operators exist.

#### Relationships

```
Location
  └─ hasMany: Operator (1:N via location_id)
```

**Relationship Details**:
- Each Location can have multiple Operators
- Each Operator belongs to exactly one Location
- Population: Operators are NOT populated when fetching Location (too heavy)

#### Validation Rules

- `display_name` must be unique across all locations
- `display_name` max length: 255 characters
- `address` must be valid (see IAddress validation)
- Cannot delete Location if Operators exist with this location_id

---

## Use Cases

### 1. CreateLocation

**Description**: Creates a new funeral home location.

**Actor**: Operator (requires role: ADMIN)

**Input**:
```typescript
{
  operator_session_id: string,
  display_name: string,
  address: IAddress,
}
```

**Output**:
```typescript
Result<ILocation, NotLoggedError | DuplicateNameError | Error>
```

**Business Logic**:
1. Validate operator session (must be logged in)
2. Check role (ADMIN only)
3. Validate display_name uniqueness
4. Validate address structure
5. Create Location entity via factory
6. Persist to database
7. Audit log: CREATE operation

**Errors**:
- `NotLoggedError` - Invalid/expired session
- `DuplicateNameError` - Name already exists
- `ValidationError` - Invalid address

---

### 2. UpdateLocation

**Description**: Updates an existing location's name or address.

**Actor**: Operator (requires role: ADMIN)

**Input**:
```typescript
{
  operator_session_id: string,
  location_id: string,
  display_name?: string,
  address?: IAddress,
}
```

**Output**:
```typescript
Result<ILocation, NotLoggedError | NotFoundError | Error>
```

**Business Logic**:
1. Validate session and role
2. Find location by ID
3. If name changed, check uniqueness
4. Update entity fields
5. Persist changes
6. Audit log: UPDATE operation

---

### 3. DeleteLocation

**Description**: Permanently removes a location.

**Actor**: Operator (requires role: ADMIN)

**Input**:
```typescript
{
  operator_session_id: string,
  location_id: string,
}
```

**Output**:
```typescript
Result<void, NotLoggedError | NotFoundError | CannotDeleteError | Error>
```

**Business Logic**:
1. Validate session and role
2. Find location by ID
3. Check if any operators reference this location (if yes, reject)
4. Hard delete from database
5. Audit log: DELETE operation

**Errors**:
- `CannotDeleteError` - Has related operators

---

### 4. GetLocation

**Description**: Retrieves a single location by ID.

**Actor**: Operator (any role)

**Input**:
```typescript
{
  operator_session_id: string,
  location_id: string,
}
```

**Output**:
```typescript
Result<ILocation, NotLoggedError | NotFoundError | Error>
```

**Business Logic**:
1. Validate session
2. Find by ID
3. Return location DTO

---

### 5. ListLocations

**Description**: Lists all locations (paginated).

**Actor**: Operator (any role)

**Input**:
```typescript
{
  operator_session_id: string,
  page?: number,
  limit?: number,
}
```

**Output**:
```typescript
Result<Page<ILocation>, NotLoggedError | Error>
```

**Business Logic**:
1. Validate session
2. Query all locations (no filters for now)
3. Apply pagination
4. Return page of DTOs

---

## Repository Interface

```typescript
interface ILocationRepo {
  create(ctx: ITransactionContext, entity: Location): Promise<Result<void, Error>>;
  
  findById(ctx: ITransactionContext, id: string): Promise<Maybe<Location>>;
  
  update(ctx: ITransactionContext, entity: Location): Promise<Result<void, Error>>;
  
  delete(ctx: ITransactionContext, id: string): Promise<Result<void, Error>>;
  
  list(
    ctx: ITransactionContext,
    options: IPaginationOptions
  ): Promise<Result<Page<Location>, Error>>;
  
  existsByDisplayName(ctx: ITransactionContext, name: string): Promise<boolean>;
}
```

---

## Database Schema

**Collection Name**: `locations`

**Document Structure**:
```typescript
{
  _id: ObjectId,
  display_name: string,
  address: {
    street: string,
    city: string,
    state: string,
    postal_code: string,
    country: string,
  },
  created_at: Date,
}
```

**Indexes**:
- `{ _id: 1 }` - Primary key
- `{ display_name: 1 }` - Unique, for name validation and searches

---

## Integration Points

### Admin Webapp

**Routes**:
- `GET /admin/locations` - List all locations
- `GET /admin/locations/new` - Create form
- `GET /admin/locations/:id` - Detail/edit view
- `POST /api/locations` - Create action
- `PATCH /api/locations/:id` - Update action
- `DELETE /api/locations/:id` - Delete action

**Loader Data**:
```typescript
// admin.locations._index.tsx
{
  locations: Page<ILocation>,
}

// admin.locations.$id.tsx
{
  location: ILocation,
}
```

### Client Webapp

Not exposed (internal admin feature only).

---

## Audit Requirements

- **CREATE**: Verb = CREATE, Title = "Nuova Location"
- **UPDATE**: Verb = UPDATE, Title = "Modifica Location"
- **DELETE**: Verb = DELETE, Title = "Elimina Location"

Metadata:
- Include `display_name` in metadata
- For updates, log old vs new values

---

## Implementation Checklist

- [x] Create entity in `/src/entity/Location.ts`
- [x] Create DTO interface in `/src/dto/ILocation.ts`
- [x] Create document type in `/src/db/Documents/LocationDoc.ts`
- [x] Create entity mapper in `/src/mapper/LocationMapper.ts`
- [x] Create repo interface in `/src/repo/ILocationRepo.ts`
- [x] Create repo implementation in `/src/repo/impl/LocationRepoImpl.ts`
- [x] Add DI symbols in `/src/di/Symbols.ts`
- [x] Register bindings in `/src/di/container.ts`
- [x] Create use case interfaces in `/src/useCase/location/`
- [x] Create use case implementations in `/src/useCase/location/impl/`
- [x] Add audit decorators to create/update/delete use cases
- [x] Create admin routes in `/packages/admin-webapp/app/routes/admin.locations.*`
- [x] Run typecheck
- [x] Document in `/packages/doc/content/entity/location.md`

---

## Notes

- IAddress is a value object defined in `/src/value_object/Address.ts`
- Location is simple but foundational - many entities will reference it
- No need for soft delete since deletion is prevented if operators exist
- Future: Could add "inactive" flag if locations close but need historical data
