# Spec Bootstrap — Reference

## Output quality rules

- **No implementation details** — no ORM syntax, no HTTP status codes, no framework APIs
- **No vague language** — avoid "should", "might", "appropriate". Use "must", "shall", "never"
- **Every requirement must be testable** — ask: how would you verify this in a test?
- **Acceptance criteria format** — WHEN/THEN: `WHEN customerId is not found THEN throw UserNotFoundError`
- **DTOs are named explicitly** — never just say "the input object"
- **Errors are named** — never just say "throw an error"

---

## DTO split rules

Define the minimum set of DTOs needed. More DTOs add surface area — only split when the shapes genuinely differ.

| Scenario                                  | DTOs to define                                                   |
|-------------------------------------------|------------------------------------------------------------------|
| Simple entity (no partial update)         | `Create[Entity]InputDto` + `[Entity]Dto`                         |
| Entity with partial update                | `Create[Entity]InputDto` + `Update[Entity]InputDto` + `[Entity]Dto` |
| Read-only use case                        | `[Entity]Dto` only                                               |
| Command with no return value              | `[VerbNoun]InputDto` + `void`                                    |

**Rules of thumb:**
- Always define a separate `[Entity]Dto` (read) — the server-assigned fields (`id`, `createdAt`) never appear in input DTOs.
- Only add `Update[Entity]InputDto` when the partial update accepts a genuinely different field set than creation (e.g. immutable fields like `customerId` are not updatable).
- Avoid a proliferation of near-identical DTOs. If two shapes are identical, use one.

---

## Repository interface hints — format

Do NOT generate a separate spec file for repository interfaces. Instead, add a `## Repository interface hints` section at the bottom of each use case spec. The hints list the exact method signatures the use case will need, and become the source of truth when generating the repository interface in the persistence layer.

Format — one line per method, TypeScript signature style:

```
## Repository interface hints

- `IInvoiceRepository.findById(id: string): Promise<Invoice | null>`
- `IInvoiceRepository.save(invoice: Invoice): Promise<void>`
- `ICustomerRepository.findById(id: string): Promise<Customer | null>`
```

One block per use case spec. If two use cases need the same method, list it in both — the persistence skill deduplicates when generating the interface.

---

## Stack adaptation notes

Tailor the constitution to the project's actual choices:

- **DI**: If using Inversify, document the `BILLING_[ROLE]` token naming pattern. If not using DI, document how dependencies are passed.
- **Validation**: Name the library once in the constitution (`Zod`, `class-validator`, or manual guards). All use case specs then inherit this choice — do not repeat it in each use case.
- **Error base class**: If the project has a `DomainError` base, name it. If not, note that all domain errors extend `Error` directly with an explicit `code` property.
- **Value objects**: If `Money`, `Address`, or similar VOs are shared, list them in the constitution's "What belongs in core" section so they are not duplicated in entity specs.
