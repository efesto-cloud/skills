# Use Case Spec Template

## Usage
One file per use case. This is the most important spec in the core.
It defines intent, boundaries, and failure modes precisely enough
that an AI agent can implement it without asking follow-up questions.

---

```markdown
---
use-case: [VerbNounUseCase]
status: draft
module: [module-name]
entity: [PrimaryEntity]
---

# Use Case: [VerbNounUseCase]

## Intent
[One sentence: what business goal does this use case achieve, from the
user's or system's perspective? Start with a verb. E.g. "Allow a customer
to place a new order in draft status."]

## Dependencies (injected via Inversify)

| Token                     | Interface                  | Used for                          |
|---------------------------|----------------------------|-----------------------------------|
| `ORDER_REPOSITORY`        | `IOrderRepository`         | Persisting and loading orders     |
| `USER_REPOSITORY`         | `IUserRepository`          | Verifying customer exists         |
| `[TOKEN]`                 | `[IService]`               | [purpose]                         |

## Input

**DTO:** `[VerbNoun]InputDto`

| Field         | Type       | Required | Rules                              |
|---------------|------------|----------|------------------------------------|
| [field]       | [type]     | yes/no   | [format, range, allowed values]    |

## Output

**DTO:** `[Entity]Dto` (or `void` if no return value)

[If meaningful: note which fields are always present vs optional in the output]

## Steps

Ordered sequence of what the use case does. Plain English — no code.

1. Validate [field] is [rule] — throw `[ErrorName]` if not
2. Load [Entity] by [field] via `I[Entity]Repository.findById()` — throw `[EntityNotFoundError]` if null
3. [Business logic step — what is computed or checked]
4. [Mutation step — what changes on the entity or aggregate]
5. Persist via `I[Entity]Repository.save()`
6. Return mapped `[Entity]Dto`

**Note on ordering:** validation before any I/O, I/O before mutations,
persist last before returning.

## Errors

| Error                         | Condition                                      |
|-------------------------------|------------------------------------------------|
| `[Entity]NotFoundError`       | Entity with given id does not exist            |
| `[Field]ValidationError`      | [Field] does not meet [rule]                   |
| `Invalid[Entity]StatusError`  | Entity is in a state that forbids this action  |
| `UnauthorizedError`           | Caller does not have permission (if applicable)|

## Acceptance criteria

WHEN/THEN format. Each line must be independently testable.

- WHEN input is valid and entity exists THEN return `[Entity]Dto` with updated state
- WHEN [field] is missing or invalid THEN throw `[ValidationError]` before any I/O
- WHEN entity does not exist THEN throw `[EntityNotFoundError]`
- WHEN entity is in status `[x]` THEN throw `Invalid[Entity]StatusError`
- WHEN repository throws THEN propagate as `RepositoryError` (do not swallow)

## Does NOT

Explicit scope boundary. List what adjacent concerns are out of scope.
This section prevents an AI agent from adding unrequested behaviour.

- Does not send notifications or emails (that is an application service concern)
- Does not handle [related but separate concern]
- Does not validate [thing validated elsewhere]
- Does not call other use cases directly

## Repository interface hints

Methods this use case will need from each injected repository.
These hints are the source of truth for what goes into the repo interface.

- `I[Entity]Repository.findById(id: string): Promise<[Entity] | null>`
- `I[Entity]Repository.save(entity: [Entity]): Promise<void>`
- `I[Other]Repository.findById(id: string): Promise<[Other] | null>`

## Open questions / assumptions ⚠️
- [Any behaviour that was assumed and needs confirmation]
- [Any edge case that was not specified and needs a decision]
```
