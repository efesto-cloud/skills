# Use Cases Index

All business operations organized by domain. Each use case describes what actors can do.

---

## Provino Domain

### CRUD Operations
- [CreateProvino](./CreateProvino.md) - Create new memorial plate draft
- [UpdateProvino](./UpdateProvino.md) - Update basic info (nome, cognome, dates, etc.)
- [DeleteProvino](./DeleteProvino.md) - Soft delete provino (ADMIN only)
- [GetProvino](./GetProvino.md) - Retrieve single provino by ID
- [SearchProvini](./SearchProvini.md) - Fuzzy search with filters

### Element Management
- [AddElementoToProvino](./AddElementoToProvino.md) - Add positioned element
- [UpdateElementoInProvino](./UpdateElementoInProvino.md) - Update position/properties
- [RemoveElementoFromProvino](./RemoveElementoFromProvino.md) - Remove element
- [DuplicateElementoInProvino](./DuplicateElementoInProvino.md) - Duplicate positioned element
- [ReorderElementsInProvino](./ReorderElementsInProvino.md) - Change z-index ordering

### Advanced Operations
- [DuplicateProvino](./DuplicateProvino.md) - Clone entire provino with all elements
- [GenerateProvinoFromModello](./GenerateProvinoFromModello.md) - Create from template

**Status**: Most implemented, template generation planned

---

## ImpresaFunebre Domain

### Account Management
- [CreateImpresa](./CreateImpresa.md) - Register new funeral home
- [UpdateImpresa](./UpdateImpresa.md) - Update business info
- [DeleteImpresa](./DeleteImpresa.md) - Soft delete (sets stato=ELIMINATO)
- [RestoreImpresa](./RestoreImpresa.md) - Restore soft-deleted impresa

### Authentication & Access
- [LoginImpresa](./LoginImpresa.md) - Password-based login
- [LogoutImpresa](./LogoutImpresa.md) - Invalidate session
- [ResetPasswordImpresa](./ResetPasswordImpresa.md) - Admin-initiated password reset (rate-limited)
- [RevokeAccessImpresa](./RevokeAccessImpresa.md) - Set stato=REVOCATO

### Search & List
- [SearchImprese](./SearchImprese.md) - Search with filters (include deleted)
- [ListImprese](./ListImprese.md) - Paginated list

**Status**: Implemented

---

## Elemento Domain

### CRUD Operations
- [CreateElemento](./CreateElemento.md) - Create design element
- [UpdateElemento](./UpdateElemento.md) - Update name, description, characteristics
- [DeleteElemento](./DeleteElemento.md) - Soft delete
- [GetElemento](./GetElemento.md) - Get by ID
- [SearchElementi](./SearchElementi.md) - Search by name, filter by characteristics

### Variante Management
- [AddVarianteToElemento](./AddVarianteToElemento.md) - Add color/size variation
- [UpdateVarianteInElemento](./UpdateVarianteInElemento.md) - Update variante properties
- [RemoveVarianteFromElemento](./RemoveVarianteFromElemento.md) - Remove variante

**Status**: Implemented

---

## Caratteristica Domain

### CRUD Operations
- [CreateCaratteristica](./CreateCaratteristica.md) - Create category/characteristic
- [UpdateCaratteristica](./UpdateCaratteristica.md) - Update name, type
- [DeleteCaratteristica](./DeleteCaratteristica.md) - Soft delete
- [GetCaratteristica](./GetCaratteristica.md) - Get by ID
- [GetCaratteristicaTree](./GetCaratteristicaTree.md) - Get hierarchical tree
- [ReorderCaratteristiche](./ReorderCaratteristiche.md) - Update order field

### Valore Management
- [AddValoreToCaratteristica](./AddValoreToCaratteristica.md) - Add value option
- [UpdateValoreInCaratteristica](./UpdateValoreInCaratteristica.md) - Update value
- [RemoveValoreFromCaratteristica](./RemoveValoreFromCaratteristica.md) - Remove value

**Status**: Implemented

---

## Catalogo Domain

### CRUD Operations
- [CreateCatalogo](./CreateCatalogo.md) - Create catalog
- [UpdateCatalogo](./UpdateCatalogo.md) - Update name, description
- [DeleteCatalogo](./DeleteCatalogo.md) - Soft delete
- [GetCatalogo](./GetCatalogo.md) - Get by ID
- [ListCataloghi](./ListCataloghi.md) - List with state filter
- [PublishCatalogo](./PublishCatalogo.md) - Set state=published
- [UnpublishCatalogo](./UnpublishCatalogo.md) - Set state=draft

### Section Management
- [AddSezioneInCatalogo](./AddSezioneInCatalogo.md) - Add section
- [UpdateSezioneInCatalogo](./UpdateSezioneInCatalogo.md) - Update section
- [RemoveSezioneInCatalogo](./RemoveSezioneInCatalogo.md) - Remove section
- [ReorderSezioniInCatalogo](./ReorderSezioniInCatalogo.md) - Reorder sections

### Item Management
- [AddItemToSezione](./AddItemToSezione.md) - Add elemento reference to section
- [RemoveItemFromSezione](./RemoveItemFromSezione.md) - Remove item

**Status**: Implemented

---

## Operator Domain

### Account Management
- [CreateOperator](./CreateOperator.md) - Create staff account (ADMIN only)
- [UpdateOperator](./UpdateOperator.md) - Update operator info
- [DeleteOperator](./DeleteOperator.md) - Hard delete (ADMIN only, cannot delete self)
- [GetOperator](./GetOperator.md) - Get by ID
- [ListOperators](./ListOperators.md) - List all operators

### Authentication
- [LoginOperator](./LoginOperator.md) - Password-based login
- [LogoutOperator](./LogoutOperator.md) - Invalidate session
- [ChangePasswordOperator](./ChangePasswordOperator.md) - Self-service password change

**Status**: Implemented

---

## Location Domain

### CRUD Operations
- [CreateLocation](./CreateLocation.md) - Create service location (ADMIN only)
- [UpdateLocation](./UpdateLocation.md) - Update name, address
- [DeleteLocation](./DeleteLocation.md) - Hard delete (cannot delete if has operators)
- [GetLocation](./GetLocation.md) - Get by ID
- [ListLocations](./ListLocations.md) - List all locations

**Status**: Implemented

---

## File Management

### Upload & Storage
- [UploadFile](./UploadFile.md) - Upload file with category-specific processing
- [DeleteFile](./DeleteFile.md) - Delete from storage and database
- [GetFile](./GetFile.md) - Retrieve file metadata
- [GetPresignedUrl](./GetPresignedUrl.md) - Get temporary download URL (S3)

### Special Processing
- [SimplifySVG](./SimplifySVG.md) - Process vector images (normalize, extract viewBox)
- [ExtractFontMetrics](./ExtractFontMetrics.md) - Extract x-height ratio from font files

**Status**: Implemented

---

## Audit & Reporting

### Audit Log
- [SearchAuditLogs](./SearchAuditLogs.md) - Search audit trail by actor, entity, verb, date
- [GetAuditLogsByEntity](./GetAuditLogsByEntity.md) - Get history for specific entity

**Note**: Audit logs are auto-created via `@audit` decorator. No manual creation.

**Status**: Implemented

---

## Modello Domain

### CRUD Operations
- [CreateModello](./CreateModello.md) - Create template provino
- [UpdateModello](./UpdateModello.md) - Update template
- [DeleteModello](./DeleteModello.md) - Soft delete
- [GetModello](./GetModello.md) - Get by ID
- [ListModelli](./ListModelli.md) - List templates
- [DuplicateModello](./DuplicateModello.md) - Clone template

**Status**: Partially implemented

---

## Drafts & Planning

Planned use cases:

- [ ] ExportProvinoPDF - Generate PDF from provino
- [ ] ExportProvinoPNG - Render provino as image
- [ ] SendProvinToClient - Email preview to funeral home
- [ ] BulkUploadElementi - CSV import for elements
- [ ] GenerateQuote - Calculate pricing from provino elements

See [../drafts/](../drafts/) for detailed planning notes.

---

**Writing a new use case?**
1. Create `UseCaseName.md` in this directory
2. Use the conversational format: "As an [actor], I want to..."
3. Link to related [entities](../entities/)
4. Add entry to this index
5. Mark status: 🔵 Draft | 🟡 Review | 🟢 Approved | ⚪ Implemented
