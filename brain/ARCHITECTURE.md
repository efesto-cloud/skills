# Core Package - Architecture Map

> **Last Updated**: 2026-04-06  
> **Purpose**: Birds-eye view of the domain. Quick reference for developers and LLMs.

**This is a living document** - Update when entities or relationships change.

---

## 📚 Full Documentation

For detailed specs, see the [specs/](./specs/) directory:

- **[specs/entities/](./specs/entities/)** - Detailed entity specifications (one file per entity)
- **[specs/usecases/](./specs/usecases/)** - Use case specifications (one file per operation)
- **[specs/drafts/](./specs/drafts/)** - Raw notes, feature requests, known issues
- **[specs/plans/](./specs/plans/)** - Implementation roadmaps (big features)
- **[specs/README.md](./specs/README.md)** - Documentation system overview
- **[specs/HEALTHCHECK.md](./specs/HEALTHCHECK.md)** - ⚕️ Periodic maintenance checklist

This file provides a **quick reference overview**. Click through to detailed specs for more.

---

## Quick Domain Overview

```
ImpresaFunebre (funeral home)
  └─ creates → Provino (memorial plate draft)
       └─ embeds → ElementoProvino[] (positioned design elements)
            └─ references → Elemento → Variante

Elemento (design element: text/image/shape)
  ├─ has many → Varianti (variations with files/pricing)
  └─ categorized by → Caratteristica (hierarchical categories)

Operator (staff/admin)
  └─ manages everything, belongs to Location

Catalogo (catalog structure)
  └─ organizes → Elementi in hierarchical sections

FileMetadata (abstract file storage)
  └─ polymorphic → ImageMetadata | VectorImageMetadata | FontMetadata | STLMetadata

AuditLog (automatic trail via @audit decorator)
```

---

## Entities

### Provino
**Aggregate Root** | `provinos` | Soft Delete: ✅ | **[Full Spec →](./specs/entities/Provino.md)**

Main composition entity. Memorial plate draft with positioned design elements.

```
_id, nome, cognome, menzione?, data_nascita, data_decesso, cimitero,
foto_file_id?, dimensioni{larghezza_mm, altezza_mm}, materiale_id?,
elementi[] (ElementoProvino), impresa_id, note?, created_at, deleted_at?
```

**Relationships**:
- BelongsTo: ImpresaFunebre (via `impresa_id`)
- References: Materiale (via `materiale_id`, can populate)
- References: FileMetadata for photo (via `foto_file_id`, can populate)
- Embeds: ElementoProvino[] with transform data (x, y, width, height, rotation, z_index)

**Use Cases**: Create, Update, Delete, Get, List, Search, AddElemento, UpdateElemento, RemoveElemento, DuplicateElemento, Duplicate (whole provino)

**Notes**: 
- Dates are free-form strings (not validated)
- Counter per impresa (auto-increment)
- Elements can be text, images, or shapes with positioning
- Text elements use `fontSize_mm` (millimeters) with `x_height_ratio` for precise sizing

---

### ImpresaFunebre
**Entity** | `impresa_funebres` | Soft Delete: ✅ (via stato)

Funeral home business entity. Client organization that creates provini.

```
_id, nome, email, telefono, indirizzo?, stato, password_hash,
reset_at?, created_at, deleted_at?
```

**Stato**: `"ATTIVO" | "REVOCATO" | "ELIMINATO"`

**Relationships**:
- HasMany: Provino (via `impresa_id`)
- HasMany: LoginSession

**Use Cases**: Create, Update, Delete, Restore, Login, Logout, ResetPassword, RevokeAccess, Search, List

**Notes**:
- Authentication via password + session cookies
- `reset_at` tracks password reset timestamp (rate-limited)
- Soft delete via `stato` field + `deleted_at`
- Cannot hard delete (preserve audit trail)

---

### Elemento
**Entity** | `elementos` | Soft Delete: ✅

Design element (product). Can be image, text, or shape. Contains variations.

```
_id, tipo, nome, descrizione?, varianti[] (IElemento.Variante),
caratteristiche[] (characteristic IDs), created_at, deleted_at?
```

**Tipo**: `"IMMAGINE" | "TESTO" | "FORMA"`

**Relationships**:
- HasMany: Variante (embedded in `varianti[]`)
- ReferencesMany: Caratteristica (via `caratteristiche[]` IDs)
- ReferencedBy: ElementoProvino (in provini)
- ReferencedBy: CatalogoItem

**Use Cases**: Create, Update, Delete, Get, List, Search, AddVariante, UpdateVariante, RemoveVariante

**Notes**:
- Varianti hold file references and pricing
- Each variante has color, dimensions, file_id, prezzo_cents
- Caratteristiche are used for filtering/categorization

---

### Caratteristica
**Entity** | `caratteristicas` | Soft Delete: ✅

Hierarchical category/characteristic system. Used to organize and filter elements.

```
_id, nome, descrizione?, tipo, valori[] (ICaratteristica.Valore),
parent_id?, order, created_at, deleted_at?
```

**Tipo**: `"HEX_COLOR" | "SINGLE_CHOICE" | "MULTI_CHOICE" | "TEXT" | "NUMBER"`

**Relationships**:
- BelongsTo: Caratteristica (self-reference via `parent_id` for tree)
- HasMany: Caratteristica (children)
- Embeds: CaratteristicaValore[] with labels and metadata

**Use Cases**: Create, Update, Delete, Get, List, Tree, Reorder, AddValore, UpdateValore, RemoveValore

**Notes**:
- Tree structure for hierarchical categories
- `order` field for manual sorting
- `HEX_COLOR` type for color pickers
- Valori hold label and optional metadata per type

---

### Operator
**Entity** | `operators` | Soft Delete: ❌

Staff/admin user. Manages the system.

```
_id, nome, cognome, email, password_hash, role, location_id, created_at
```

**Role**: `"ADMIN" | "OPERATOR"`

**Relationships**:
- BelongsTo: Location (via `location_id`)
- HasMany: LoginSession

**Use Cases**: Create, Update, Delete, Get, List, Login, Logout, ChangePassword

**Notes**:
- ADMIN role required for sensitive operations (delete, settings)
- Authentication via password + session cookies
- `ENABLE_AUTOLOGIN` env var for demo operator access

---

### Location
**Entity** | `locations` | Soft Delete: ❌ | **[Full Spec →](./specs/entities/Location.md)**

Physical funeral service location. Each operator belongs to one.

```
_id, display_name, address{street, city, state, postal_code, country}, created_at
```

**Relationships**:
- HasMany: Operator (via `location_id`)

**Use Cases**: Create, Update, Delete, Get, List

**Notes**:
- Simple entity, no soft delete
- Cannot delete if operators exist (foreign key constraint)
- `display_name` must be unique

---

### Catalogo
**Aggregate Root** | `catalogos` | Soft Delete: ✅

Hierarchical catalog structure for organizing elements.

```
_id, name, description?, state, sections[] (ICatalogo.Sezione), created_at, deleted_at?
```

**State**: `"draft" | "published"`

**Relationships**:
- Contains: SezioneCatalogo[] (nested tree structure)
- Sections contain: CatalogoItem[] (references to Elemento)

**Use Cases**: Create, Update, Delete, Get, List, Publish, Unpublish, ReorderSections, AddSezione, UpdateSezione, RemoveSezione, AddItem, RemoveItem

**Notes**:
- Tree structure: sections can have children sections
- Items reference Elemento with optional override data
- `order` field per section and per item
- Only published catalogs visible to clients

---

### Defunto  
**Entity** | `defuntos` | Soft Delete: ❌

Deceased person record. Simplified - not used heavily in current workflow.

```
_id, nome, cognome, data_nascita, data_decesso, foto_file_id?, impresa_id
```

**Relationships**:
- BelongsTo: ImpresaFunebre (via `impresa_id`)

**Use Cases**: Create, Update, Get, List, Search

**Notes**:
- Originally designed as separate entity, now mostly data fields in Provino
- Dates are free-form strings
- Not heavily used (provino embeds this data directly)

---

### FileMetadata
**Entity** | `file_metadatas` | Soft Delete: ❌

Abstract file storage. Polymorphic based on category.

```
_id, filename, content_type, size_bytes, storage_key (S3 or local path),
category, upload_date, metadata (polymorphic by category)
```

**Category**: `"IMAGE_RASTER" | "IMAGE_VECTOR" | "FONT" | "STL" | "DOCUMENT" | "TEXTURE"`

**Relationships**:
- HasOne: ImageMetadata | VectorImageMetadata | FontMetadata | TextureMetadata (polymorphic)

**Use Cases**: Upload, Delete, Get, List, GetPresignedUrl

**Notes**:
- `storage_key` unique (prevents duplicates)
- S3 storage in prod, local filesystem in dev
- Metadata field structure varies by category:
  - IMAGE_RASTER: width, height, format
  - IMAGE_VECTOR: viewBox, simplified flag
  - FONT: family, weight, style, x_height_ratio
  - STL: vertices_count, volume_mm3

---

### AuditLog
**Entity** | `audit_logs` | Soft Delete: ❌

Automatic audit trail. Created via `@audit` decorator on use cases.

```
_id, actor{type, id}, verb, entity{type, id?}, title, sentence,
metadata (Map<string, any>), timestamp, duration_ms
```

**Actor Type**: `"operator" | "impresa"`  
**Verb**: `"CREATE" | "UPDATE" | "DELETE" | "LOGIN" | "LOGOUT" | "UPLOAD" | "PUBLISH" | ...`

**Relationships**:
- References: Operator | ImpresaFunebre (via `actor.id`)
- References: Any Entity (via `entity.id`)

**Use Cases**: Search, List, GetByEntity (auto-created via decorator)

**Notes**:
- Auto-generates Italian sentence: "L'operatore Mario ha creato un Provino."
- All data-modifying use cases must use `@audit` decorator
- Read operations (GET, LIST, SEARCH) are NOT audited
- TTL index for automatic cleanup (e.g., 90 days)

---

### Materiale
**Entity** | `materiales` | Soft Delete: ✅

Material/background options for provini.

```
_id, nome, descrizione?, texture_file_id?, colore?, created_at, deleted_at?
```

**Relationships**:
- References: FileMetadata for texture (via `texture_file_id`)
- ReferencedBy: Provino (via `materiale_id`)

**Use Cases**: Create, Update, Delete, Get, List

**Notes**:
- Can have texture image or solid color
- Used as background in compositore

---

### Modello
**Aggregate Root** | `modellos` | Soft Delete: ✅

Template provino. Pre-configured layouts.

```
_id, nome, descrizione?, dimensioni{larghezza_mm, altezza_mm},
elementi[] (ElementoModello), created_at, deleted_at?
```

**Relationships**:
- Embeds: ElementoModello[] (similar to ElementoProvino)
- UsedBy: Provino.createFromModello()

**Use Cases**: Create, Update, Delete, Get, List, Duplicate

**Notes**:
- Template for creating provini
- Similar structure to Provino but without deceased person data
- Can be duplicated to create variants

---

## Value Objects

### IAddress
```typescript
{ street: string, city: string, state: string, postal_code: string, country: string }
```
Used in: Location, ImpresaFunebre

### IProvino.Dimensioni / IModello.Dimensioni
```typescript
{ larghezza_mm: number, altezza_mm: number }
```
Used in: Provino, Modello

### IElementoProvino.Transform / IElementoModello.Transform
```typescript
{ x_mm: number, y_mm: number, width_mm: number, height_mm: number, rotation_deg: number, z_index: number }
```
Used in: ElementoProvino, ElementoModello

### IElementoProvino.TextProperties
```typescript
{ fontFamily: string, fontSize_mm: number, x_height_ratio: number, content: string, color?: string }
```
Used in: ElementoProvino (when tipo = "TESTO")

---

## Type System

**Key Type Unions**:

| Type | Values | Dict? |
|------|--------|-------|
| `TProvinableState` | `"draft"`, `"published"` | ✅ |
| `TElementoTipo` | `"IMMAGINE"`, `"TESTO"`, `"FORMA"` | ✅ |
| `TCaratteristicaTipo` | `"HEX_COLOR"`, `"SINGLE_CHOICE"`, `"MULTI_CHOICE"`, `"TEXT"`, `"NUMBER"` | ✅ |
| `TOperatorRole` | `"ADMIN"`, `"OPERATOR"` | ✅ |
| `TImpresaStato` | `"ATTIVO"`, `"REVOCATO"`, `"ELIMINATO"` | ✅ |
| `TFileCategory` | `"IMAGE_RASTER"`, `"IMAGE_VECTOR"`, `"FONT"`, `"STL"`, `"DOCUMENT"`, `"TEXTURE"` | ✅ |
| `TAuditVerb` | `"CREATE"`, `"UPDATE"`, `"DELETE"`, `"LOGIN"`, `"LOGOUT"`, `"UPLOAD"`, `"PUBLISH"`, ... | ✅ |

**Pattern**: Type (compile-time) → Enum (runtime) → Dict (labels/descriptions)

---

## Services

### IFileStorageService
Upload, download, delete files. S3 (prod) or local filesystem (dev).

### IEmailService
Send transactional emails (OTP, welcome, password reset). React-based templates.

### ITerminalLocationService
Business logic for Location validation.

### IOTPService
Generate and validate one-time passwords for login.

---

## Database

**Collections & Key Indexes**:

| Collection | Primary Indexes |
|------------|-----------------|
| `provinos` | `impresa_id + deleted_at`, `cimitero + deleted_at`, text search on nome/cognome/cimitero |
| `impresa_funebres` | `email` (unique), `stato + deleted_at` |
| `elementos` | `deleted_at`, `caratteristiche` (array) |
| `caracteristicas` | `parent_id + order`, `deleted_at` |
| `operators` | `email` (unique), `location_id` |
| `locations` | `display_name` (unique) |
| `catalogos` | `state + deleted_at` |
| `file_metadatas` | `storage_key` (unique), `category` |
| `audit_logs` | `timestamp` (TTL), `actor.type + actor.id`, `entity.type + entity.id` |
| `login_sessions` | `operator_id`, `impresa_id`, `expires_at` (TTL) |

---

## Architecture Patterns

### Use Case Pattern
All use cases implement `IUseCase<TRequest, TResponse>` with:
- `name: string` (auto from class name)
- `execute(input): Promise<output>`

Auth wrappers:
- `WithOperatorAuth<T>` - Requires operator session
- `WithImpresaAuth<T>` - Requires impresa session
- No wrapper - Public (login, etc.)

### Audit Decorator
```typescript
@audit<IUseCaseInterface>({
  entity: EntityClass,
  verb: "CREATE" | "UPDATE" | "DELETE" | ...,
  title: "Italian description",
  onOutput?: (output, context) => { context.setEntityId(output.data?._id); }
})
```

**Required on**: All data-modifying operations  
**Not on**: Read operations (GET, LIST, SEARCH)

### Repository Pattern
Standard interface:
```typescript
create(ctx, entity): Promise<Result<void, Error>>
findById(ctx, id, options?): Promise<Maybe<Entity>>
update(ctx, entity): Promise<Result<void, Error>>
delete/softDelete(ctx, id): Promise<Result<void, Error>>
search(ctx, filters, pagination): Promise<Result<Page<Entity>, Error>>
```

### Population System
Entities with relationships support population via aggregation `$lookup`:
- Provino can populate: `materiale`, `foto`
- ElementoProvino can populate: `elemento`, `variante`

Pattern: `{ populate: ["materiale", "foto"] }` in repo options

---

## Entry Points

**@dav/core/server**: Full server-side (DB, use cases, repos)  
**@dav/core/client**: DTOs, types, enums, dicts only  
**@dav/core/init**: DB initialization and container setup

---

## Adding New Features

1. **New Entity**: Update this file → Create spec → Implement Entity → DTO → Document → Mapper → Repo → Use Cases → DI → Routes → Docs
2. **New Use Case**: Update entity section here → Create interface → Implementation → Audit decorator → DI → Route
3. **New Relationship**: Update both entities here → Update documents → Update mappers → Add population if needed

---

## 📋 Documentation Organization

This file provides a **scannable overview**. For detailed information:

1. **Entity details** → [specs/entities/](./specs/entities/) - One file per entity
2. **Use case details** → [specs/usecases/](./specs/usecases/) - One file per operation
3. **Feature requests** → [specs/drafts/feature-requests.md](./specs/drafts/feature-requests.md)
4. **Known issues** → [specs/drafts/known-issues.md](./specs/drafts/known-issues.md)
5. **Raw notes** → [specs/drafts/](./specs/drafts/) - Drop ideas here first

**Maintenance**:
- Update this file when entities or major relationships change
- Update [specs/entities/index.md](./specs/entities/index.md) when adding entities
- Update [specs/usecases/index.md](./specs/usecases/index.md) when adding operations
- ⚕️ Run [HEALTHCHECK.md](./specs/HEALTHCHECK.md) monthly to verify alignment

---

## Dev Notes

- **Timezone**: Europe/Rome (Italian)
- **Locale**: Italian (UI, audit, errors)
- **Strict TypeScript**: All code
- **Monads**: Result/Maybe for errors, no try/catch in use cases
- **Hexagonal**: Core isolated from infrastructure

**Last Review**: 2026-04-06 | Review monthly or after major refactors
