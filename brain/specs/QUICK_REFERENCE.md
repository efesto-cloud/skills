# Quick Reference - Writing Specs

Fast answers to common questions when writing blueprints.

---

## Writing Use Cases

**Pattern**: "As an [actor], I want to [action]. [Additional details in sentences.]"

```markdown
### Search Provini

As an **operator**, I want to search provini by name or cemetery. 
The search uses fuzzy matching across multiple fields.

**Input**: `q` (search text), `page?`, `limit?`
**Returns**: Page of matching provini

**Errors**:
- NotLoggedError
```

**Actors**:
- `operator` - Requires operator session (implicit: `operator_session_id`)
- `operator (ADMIN)` - Requires ADMIN role
- `operator (role: ADMIN)` - Alternative notation
- `impresa` - Requires impresa session (implicit: `impresa_session_id`)
- `public` - No authentication needed

**Don't repeat common fields**: If actor is "operator", `operator_session_id` is implicit.

---

## Entity Properties

**Keep it simple**:
```markdown
Core properties: _id, name, state, parent_id?, created_at, deleted_at?
```

Just list them comma-separated. Types are usually obvious from context.

**Annotate special cases**:
- `email` (unique, indexed)
- `name` (max 255 chars)
- `tags[]` (array of strings)
- `metadata` (polymorphic, varies by type)

**Type notation** (when needed):
```typescript
string           // Primitive
ObjectId         // MongoDB ID
DateTime         // Luxon DateTime
string?          // Optional
IAddress         // Value object
TEntityState     // Type union
string[]         // Array
```

## Relationships

**Write in plain English**:
```markdown
**Relationships**:
- Each Provino belongs to an ImpresaFunebre (via `impresa_id`)
- Each Provino has many ElementoProvino (embedded)
- Provino references Materiale (FK only, not populated)
```

**When to populate?**
- ✅ Small related data needed often (e.g., file metadata, materials)
- ❌ Large arrays (performance hit)
- ❌ Recursive relationships (infinite loop risk)

## Soft Delete

**When to use**:
- ✅ Audit trail required
- ✅ Referenced by other entities (foreign key integrity)
- ✅ "Undo delete" feature might be needed
- ❌ Simple lookup data with no dependencies
- ❌ High-volume transient data

**How**: Add `deleted_at?: DateTime` property

---

## Type Unions

**When needed**:
```typescript
// State machine
TTaskState = "pending" | "in_progress" | "completed" | "failed"

// Categories
TElementType = "text" | "image" | "shape"

// Formatted strings
THexColor = `#${string}`
```

Just define inline in the Entity section. Create the actual files during implementation.

---

## Common Errors

**Standard error patterns**:
```markdown
**Errors**:
- NotLoggedError - Invalid/expired session
- PermissionError - Insufficient role
- NotFoundError - Entity doesn't exist
- ValidationError - Invalid input
- DuplicateError - Unique constraint violated
- CannotDeleteError - Has dependencies
```

Pick the ones that apply, skip obvious ones.

---

## Business Rules

**Write as bullets**:
```markdown
**Rules**:
- Name must be unique within parent scope
- Cannot delete if has active children
- State transitions: draft → active only (no going back)
- ADMIN role required for deletion
```

Focus on **constraints** and **what's not allowed**.

---

## Database Indexes

**When to index**:
- ✅ Foreign keys (e.g., `parent_id`)
- ✅ Unique constraints (e.g., `email`)
- ✅ Frequent filters (e.g., `state`, `deleted_at`)
- ✅ Sort fields (e.g., `created_at DESC`)
- ❌ Low-selectivity booleans
- ❌ Rarely queried fields

**Compound indexes**:
```
{ parent_id: 1, deleted_at: 1 }        // List by parent, exclude deleted
{ name: 1, parent_id: 1 }              // Unique name within parent
{ created_at: -1, deleted_at: 1 }      // Recent non-deleted items
```

---

## Audit Requirements

**When to audit**:
- ✅ CREATE, UPDATE, DELETE
- ✅ State transitions (PUBLISH, ARCHIVE)
- ✅ Permission/access changes
- ❌ Read operations (GET, LIST, SEARCH)

**Just note the verbs**:
```markdown
**Audit**: CREATE, UPDATE, DELETE, PUBLISH
```

Implementation uses `@audit` decorator automatically.

---

## What NOT to Specify

**You don't need**:
- Exact TypeScript syntax (sketch the shape)
- Every error message string
- Exact validation regex
- DI container registration code
- Mapper transformation logic
- Exact audit decorator code

**You do need**:
- What properties exist
- Business logic rules
- What operations are allowed
- Who can do what (actor + role)
- Relationships between entities
- Error cases

---

## Status Markers

```markdown
> **Status**: 🔵 Draft
```

- 🔵 **Draft** - Initial idea, gathering feedback
- 🟡 **In Review** - Ready for team review  
- 🟢 **Approved** - Start implementation
- ⚪ **Implemented** - Archived for reference

---

## Three Levels of Detail

**Level 1: Minimal** (quick idea capture)
```markdown
## Entity
name, state, parent_id?

## Operations
- Create: As operator, input name
- List: As operator, paginated
```

**Level 2: Conversational** (recommended)
```markdown
### Create EntityName

As an **operator (ADMIN)**, I want to create a new entity. 
Name must be unique.

**Input**: `name`, `description?`
**Errors**: NotLoggedError, DuplicateError
```

**Level 3: Detailed** (complex features)
Add special cases, edge cases, performance notes, implementation gotchas.

**Start minimal, add detail as you think through it.**

---

## Quick Checklist

Before starting implementation:

- [ ] Entity name and collection name decided
- [ ] Soft delete strategy decided (yes/no + why)
- [ ] Core properties listed
- [ ] Type unions defined (if needed)
- [ ] Relationships identified
- [ ] Business rules noted
- [ ] CRUD operations listed with actors
- [ ] Error cases considered
- [ ] Indexes planned
- [ ] Audit verbs listed

**Don't need all sections filled** - just enough to start coding confidently.

---

## Templates

**Pick one**:
- `TEMPLATE-MINIMAL.md` - Quick idea capture (5 minutes)
- `TEMPLATE-CONVERSATIONAL.md` - Standard blueprint (15-30 minutes)
- `TEMPLATE.md` - Structured/detailed (when you need everything organized)

**Examples**:
- `esempio-location.md` - Simple CRUD entity
- `esempio-provino-search.md` - Complex search feature

---

## Common Patterns

**Simple CRUD**:
Entity + Create + Update + Delete + List + Get

**Search Feature**:
Entity + Create + Search (with filters) + Get

**Hierarchical**:
Entity with `parent_id` + Tree operations + Reorder

**State Machine**:
Entity with state type + Transition operations (Publish, Archive, etc.)

**Soft-Deletable**:
Add `deleted_at?` + Restore operation + `include_deleted` filters

---

## Remember

**Write for humans first**: You and your team should understand it quickly.  
**Claude can infer a lot**: Types, standard patterns, common implementations.  
**Iterate**: Start rough, refine as you go.  
**Update it**: When implementation reveals better designs.

---

## Maintenance

**Keep specs aligned** with reality:
- Update specs when code changes
- Mark implemented features as ⚪
- Run [HEALTHCHECK.md](./HEALTHCHECK.md) monthly to catch drift

<Check for>:
- ✅ Implementation matches specs
- ✅ Specs reference implemented entities/usecases
- ✅ Drafts promoted or archived
- ✅ Dead links fixed
- ✅ Index files complete

**Healthy docs** = Easy to navigate, mostly accurate, links work, not too stale.

---

When in doubt, **write less** and be conversational. This is a blueprint, not a contract.
