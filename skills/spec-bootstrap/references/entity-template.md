# Entity Spec Template

## Usage
One file per entity. Keep it focused on domain meaning and invariants.
No implementation details. No ORM. No HTTP.

---

```markdown
---
entity: [EntityName]
status: draft
module: [module-name]
---

# Entity: [EntityName]

## Purpose
[One sentence: what real-world concept does this entity represent, and what
role does it play in the domain?]

## Fields

| Field       | Type              | Rules / Constraints                          |
|-------------|-------------------|----------------------------------------------|
| id          | string            | UUID v4, immutable after creation            |
| [field]     | [type]            | [required/optional, format, allowed values]  |
| status      | [StatusEnum]      | See status transitions below                 |
| createdAt   | Date              | Set on creation, never updated               |
| updatedAt   | Date              | Updated on every mutation                    |

## Status transitions (if applicable)

```
[draft] → [confirmed] → [completed]
         ↘ [cancelled]
```

Rules:
- WHEN status is `cancelled` THEN no further transitions are allowed
- WHEN transitioning to `confirmed` THEN [condition that must hold]
- [Add one rule per arrow that has a guard]

## Invariants

Business rules that must always hold, regardless of how the entity is
created or mutated. These are enforced by the entity's own methods.

- [Invariant 1: plain English, testable]
- [Invariant 2]
- WHEN [condition] THEN [what must be true]

## DTOs

| DTO Name              | Purpose                        | Fields included                    |
|-----------------------|--------------------------------|------------------------------------|
| `[Entity]Dto`         | Full read representation       | All fields                         |
| `Create[Entity]InputDto` | Create a new entity         | [list fields, exclude id/createdAt]|
| `Update[Entity]InputDto` | Partial update (if needed)  | [list mutable fields only]         |

Include `Update[Entity]InputDto` only when partial updates use a different field set than creation. See [REFERENCE.md](../../REFERENCE.md) for the DTO split decision table.

## Domain errors originating from this entity

| Error name                    | When it is thrown                              |
|-------------------------------|------------------------------------------------|
| `[Entity]NotFoundError`       | Entity with given id does not exist            |
| `Invalid[Entity]StatusError`  | Attempted an illegal status transition         |
| `[Entity]AlreadyExistsError`  | Duplicate detected on a unique field           |

## Open questions / assumptions ⚠️
- [Any field or rule that was assumed and needs user confirmation]
```
