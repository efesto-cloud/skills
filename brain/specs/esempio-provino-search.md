# Provino Search - Blueprint

> **Status**: ⚪ Implemented (example)  
> **Domain**: Provino

## What & Why

Operators need to quickly find provini (memorial plate drafts) created by funeral homes. Search should work across multiple fields (name, surname, cemetery) and support filtering by date and impresa.

---

## Entity: Provino

**Collection**: `provinos` | **Soft Delete**: Yes

### Core Properties

```
_id, nome, cognome, menzione?, data_nascita, data_decesso, cimitero, 
foto_file_id?, dimensioni, materiale_id?, elementi[], impresa_id, 
note?, created_at, deleted_at?
```

### Relationships

- Each Provino belongs to an ImpresaFunebre (via `impresa_id`)
- Each Provino may reference a Materiale (via `materiale_id`)
- Each Provino may reference a photo FileMetadata (via `foto_file_id`)
- Each Provino embeds multiple ElementoProvino items

### Business Rules

- `nome` and `cognome` are required (deceased person's name)
- Dates (`data_nascita`, `data_decesso`) are free-form strings (not validated as dates)
- `cimitero` is required (cemetery name)
- Cannot permanently delete (only soft delete)
- When deleted, all audit history is preserved

---

## What You Can Do

### Create Provino

As an **operator**, I want to create a new provino for a deceased person. The provino is assigned to an impresa and starts with basic information (name, surname, dates, cemetery).

**Input**: `nome`, `cognome`, `data_nascita`, `data_decesso`, `cimitero`, `menzione?`, `impresa_id`, `dimensioni`, `foto_file_id?`, `note?`  
**Returns**: The created provino with generated ID

**Errors**:
- NotLoggedError
- ValidationError - Missing required fields
- NotFoundError - Impresa doesn't exist

---

### Update Provino

As an **operator**, I want to update a provino's basic information (name, dates, cemetery, photo, notes). The dimensions cannot be changed after creation.

**Input**: `provino_id`, `nome?`, `cognome?`, `menzione?`, `data_nascita?`, `data_decesso?`, `cimitero?`, `foto_file_id?`, `note?`  
**Returns**: The updated provino

**Errors**:
- NotLoggedError
- NotFoundError - Provino doesn't exist or is deleted

---

### Search Provini

As an **operator**, I want to search provini by name, surname, or cemetery using a single search term. The search uses fuzzy matching across these fields. Results are paginated and can be filtered by impresa and creation date range. By default, deleted provini are excluded.

**Input**: `q?` (search text), `impresa_id?`, `created_from?`, `created_to?`, `cimitero?`, `include_deleted?`, `page?`, `limit?`  
**Returns**: Page of provini with total count

**Special Cases**:
- If `q` is empty, returns all provini (with filters applied)
- Search is case-insensitive
- Matches partial words (e.g., "mar" matches "Mario" and "Maria")
- Cemetery filter is exact match (not fuzzy)

**Errors**:
- NotLoggedError

---

### Get Provino

As an **operator**, I want to retrieve a provino by ID with all its positioned elements. The materiale and foto can be populated.

**Input**: `provino_id`, `populate?` (options: "materiale", "foto")  
**Returns**: The provino with optional populated relationships

**Errors**:
- NotLoggedError
- NotFoundError

---

### Soft Delete Provino

As an **operator (ADMIN)**, I want to soft-delete a provino. This sets `deleted_at` but preserves all data for audit purposes.

**Input**: `provino_id`  
**Returns**: void

**Errors**:
- NotLoggedError
- PermissionError - Not ADMIN role
- NotFoundError

---

### Duplicate Provino

As an **operator**, I want to duplicate an existing provino with all its elements. The new provino gets a copy of all positioned elements and their configurations, but has a new ID and creation timestamp.

**Input**: `source_provino_id`, `new_nome?`, `new_cognome?` (optional overrides)  
**Returns**: The new provino copy

**Use Case**: Funeral homes often create similar designs for the same cemetery/size.

**Errors**:
- NotLoggedError
- NotFoundError - Source provino doesn't exist

---

## Repository Interface

```typescript
interface IProvinoRepo {
  create(ctx, provino): Promise<Result<void, Error>>
  findById(ctx, id, options?): Promise<Maybe<Provino>>
  update(ctx, provino): Promise<Result<void, Error>>
  softDelete(ctx, id): Promise<Result<void, Error>>
  search(ctx, filters, pagination): Promise<Result<Page<Provino>, Error>>
  countByImpresa(ctx, impresa_id): Promise<number>
}
```

---

## Database

**Indexes**:
- `{ _id: 1 }` - Primary
- `{ impresa_id: 1, deleted_at: 1, created_at: -1 }` - List by impresa
- `{ nome: "text", cognome: "text", cimitero: "text" }` - Fuzzy search
- `{ cimitero: 1, deleted_at: 1 }` - Filter by cemetery
- `{ deleted_at: 1 }` - Soft delete queries

---

## Admin Routes

```
GET  /admin/provini                    → List/search view
GET  /admin/provini/new                → Create form
GET  /admin/provini/:id                → Detail/edit view
POST /api/provini                      → Create action
PATCH /api/provini/:id                 → Update action
DELETE /api/provini/:id                → Soft delete action
POST /api/provini/:id/duplicate        → Duplicate action
```

---

## Client Routes

```
GET  /provini                          → Client's provini list
GET  /provini/:id/composer             → Visual editor
```

---

## Audit Trail

- **CREATE**: "Nuovo Provino" (with nome/cognome in metadata)
- **UPDATE**: "Modifica Provino"
- **DELETE**: "Elimina Provino"
- **DUPLICATE**: "Duplica Provino" (with source and new IDs)

---

## Implementation Notes

- **Search performance**: Text index on nome/cognome/cimitero for fuzzy search
- **Counter**: Each impresa has a provino counter (auto-increment per impresa, not global)
- **Dates**: Stored as strings, not Date objects (funeral homes enter whatever format they want)
- **Population**: Materiale and foto are large, only populate on explicit request
- **Elements**: Embedded ElementoProvino array can grow large, consider projection for list views

---

## Open Questions

- [x] ~~Should we allow restoring deleted provini?~~ → No, ADMIN can modify deleted_at directly if needed
- [ ] Should duplicated provini link back to the original? → TBD
- [ ] Do we need provino templates (pre-configured layouts)? → Future feature
