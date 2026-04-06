# Entities Index

Quick reference to all domain entities. Click through for detailed specs.

---

## Core Entities

### [Provino](./Provino.md)
Memorial plate draft with positioned design elements. Main composition entity.

**Collection**: `provinos` | **Soft Delete**: ✅  
**Relationships**: BelongsTo ImpresaFunebre, embeds ElementoProvino[]  
**Status**: ⚪ Implemented

---

### [ImpresaFunebre](./ImpresaFunebre.md)
Funeral home business entity. Client organization.

**Collection**: `impresa_funebres` | **Soft Delete**: ✅ (via stato)  
**Relationships**: HasMany Provino  
**Status**: ⚪ Implemented

---

### [Elemento](./Elemento.md)
Design element (product). Can be image, text, or shape.

**Collection**: `elementos` | **Soft Delete**: ✅  
**Relationships**: HasMany Variante (embedded), referenced by ElementoProvino  
**Status**: ⚪ Implemented

---

### [Caratteristica](./Caratteristica.md)
Hierarchical category/characteristic system for organizing elements.

**Collection**: `caratteristicas` | **Soft Delete**: ✅  
**Relationships**: Self-referencing tree (parent_id), embeds Valori  
**Status**: ⚪ Implemented

---

### [Operator](./Operator.md)
Staff/admin user managing the system.

**Collection**: `operators` | **Soft Delete**: ❌  
**Relationships**: BelongsTo Location  
**Status**: ⚪ Implemented

---

### [Location](./Location.md)
Physical funeral service location.

**Collection**: `locations` | **Soft Delete**: ❌  
**Relationships**: HasMany Operator  
**Status**: ⚪ Implemented

---

### [Catalogo](./Catalogo.md)
Hierarchical catalog structure for organizing elements.

**Collection**: `catalogos` | **Soft Delete**: ✅  
**Relationships**: Contains SezioneCatalogo[] (tree), references Elemento  
**Status**: ⚪ Implemented

---

### [FileMetadata](./FileMetadata.md)
Abstract file storage with polymorphic metadata.

**Collection**: `file_metadatas` | **Soft Delete**: ❌  
**Relationships**: Polymorphic HasOne based on category  
**Status**: ⚪ Implemented

---

### [Materiale](./Materiale.md)
Material/background options for provini.

**Collection**: `materiales` | **Soft Delete**: ✅  
**Relationships**: References FileMetadata for texture  
**Status**: ⚪ Implemented

---

### [Modello](./Modello.md)
Template provino with pre-configured layouts.

**Collection**: `modellos` | **Soft Delete**: ✅  
**Relationships**: Embeds ElementoModello[], used by Provino  
**Status**: ⚪ Implemented

---

### [AuditLog](./AuditLog.md)
Automatic audit trail created via decorator.

**Collection**: `audit_logs` | **Soft Delete**: ❌  
**Relationships**: References Operator | ImpresaFunebre, references any Entity  
**Status**: ⚪ Implemented

---

### [Defunto](./Defunto.md)
Deceased person record (legacy, data now in Provino).

**Collection**: `defuntos` | **Soft Delete**: ❌  
**Relationships**: BelongsTo ImpresaFunebre  
**Status**: ⚪ Implemented (minimal use)

---

## Drafts & Planning

New entity specs in planning:

- [ ] None currently

See [../drafts/](../drafts/) for raw ideas and meeting notes.

---

## Quick Domain Map

```
ImpresaFunebre → creates → Provino
  └─ embeds → ElementoProvino[]
       └─ references → Elemento → Variante

Caratteristica (tree)
  └─ categorizes → Elemento

Catalogo (tree)
  └─ organizes → Elemento

Operator → manages everything
  └─ belongs to → Location

FileMetadata (polymorphic)
  └─ used by → Provino, Elemento.Variante, Materiale
```

---

**Adding a new entity?**
1. Create `entity-name.md` in this directory
2. Add entry to this index
3. Link from related entities
4. Update use cases that interact with it
