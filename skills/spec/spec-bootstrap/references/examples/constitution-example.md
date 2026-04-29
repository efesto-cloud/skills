# Core Constitution — billing

## What this package is
The `billing` core models the invoicing and payment lifecycle within the platform.
It is responsible for creating, issuing, and tracking invoices, and for recording
payment events. It belongs to the `billing` bounded context and is consumed by the
`billing-mongodb` and `billing-webapp` packages. It has no knowledge of how data is
stored or how results are rendered.

## Principles

### Purity
- No imports from infrastructure packages (no Mongoose, Stripe SDK, Express, etc.)
- No environment variable reads
- No network calls, file system access, or any I/O
- No framework-specific decorators on entities or DTOs

### Dependency injection
- DI via Inversify
- All tokens declared in `src/tokens.ts` — one export per injectable
- Constructor injection only — no property injection, no service locator pattern
- Token naming: `BILLING_[ROLE]` e.g. `BILLING_INVOICE_REPOSITORY`, `BILLING_ISSUE_INVOICE_USE_CASE`

### Use cases
- One public method: `execute(input: XInputDto): Promise<XDto>`
- No business logic outside use cases (entities hold invariants, use cases hold orchestration)
- Use cases do not call other use cases — compose via shared domain services if needed

### DTOs
- Plain TypeScript interfaces — no ORM decorators, no validation decorators
- Suffix convention: `[Entity]Dto` (read), `Create[Entity]InputDto` (write)
- DTOs live in `src/dtos/` — one file per entity

### Errors
- All domain errors extend `DomainError` base class
- Error names are explicit: `InvoiceNotFoundError`, `InvalidInvoiceStatusError`
- Use cases never throw raw `Error` — always a typed domain error
- Error codes are stable strings (e.g. `INVOICE_NOT_FOUND`)

### Validation
- Input validation happens at the use case boundary via Zod schemas
- Entities enforce invariants via methods, not constructor guards

## Naming conventions

| Concept            | Convention                        | Example                         |
|--------------------|-----------------------------------|---------------------------------|
| Entity             | PascalCase noun                   | `Invoice`, `Customer`           |
| Repository iface   | `I[Entity]Repository`             | `IInvoiceRepository`            |
| Use case class     | `[Verb][Noun]UseCase`             | `IssueInvoiceUseCase`           |
| Use case iface     | `I[Verb][Noun]UseCase`            | `IIssueInvoiceUseCase`          |
| Input DTO          | `[Verb][Noun]InputDto`            | `CreateInvoiceInputDto`         |
| Read DTO           | `[Entity]Dto`                     | `InvoiceDto`                    |
| Domain error       | `[Noun][Condition]Error`          | `InvoiceNotFoundError`          |
| DI token           | `BILLING_[ROLE]` (SCREAMING)      | `BILLING_INVOICE_REPOSITORY`    |

## What belongs in core

- `Invoice` entity and its domain methods
- `Customer` entity (read-only — owned by the `identity` core, mirrored here)
- Repository interfaces: `IInvoiceRepository`, `ICustomerRepository`
- Use case interfaces and implementations
- DTOs (`InvoiceDto`, `CreateInvoiceInputDto`, `IssueInvoiceInputDto`)
- Domain errors (`InvoiceNotFoundError`, `InvalidInvoiceStatusError`, `InvoiceAlreadyIssuedError`)
- DI tokens (`src/tokens.ts`)
- `Money` value object (amount + currency)

## What does NOT belong in core

- MongoDB models or Mongoose schemas
- HTTP handlers or route definitions
- Email or PDF invoice delivery
- Stripe SDK calls or payment gateway integration
- Authentication token generation or verification
- Environment config or secrets
- Logging implementation

## External systems this core is agnostic to

MongoDB, Stripe, SendGrid, AWS S3, any HTTP transport
