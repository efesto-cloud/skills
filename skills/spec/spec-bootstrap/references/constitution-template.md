# Constitution Template

## Usage
Fill every section. Remove placeholder comments before saving.
This file is the non-negotiable contract for the entire core package.
Every AI agent and developer touching the core must read this first.

---

```markdown
# Core Constitution — [Domain Name]

## What this package is
[One paragraph: the domain this core models, the bounded context it belongs to,
and the role it plays in the broader system.]

## Principles

### Purity
- No imports from infrastructure packages (no Mongoose, Prisma, Express, Fastify, etc.)
- No environment variable reads
- No network calls, file system access, or any I/O
- No framework-specific decorators on entities or DTOs

### Dependency injection
- DI via Inversify
- All tokens declared in `src/tokens.ts` — one export per injectable
- Constructor injection only — no property injection, no service locator pattern
- Token naming: `[DOMAIN]_[ROLE]` e.g. `ORDER_REPOSITORY`, `CREATE_ORDER_USE_CASE`

### Use cases
- One public method: `execute(input: XInputDto): Promise<XDto>`
- No business logic outside use cases (entities hold invariants, use cases hold orchestration)
- Use cases do not call other use cases — compose via shared services if needed

### DTOs
- Plain TypeScript interfaces or classes — no ORM decorators, no validation decorators
- Suffix convention: `[Entity]Dto` (read), `[Entity]InputDto` (write), `[Entity]UpdateDto` (partial update)
- DTOs live in `src/dtos/` — one file per entity

### Errors
- All domain errors extend `DomainError` base class
- Error names are explicit and descriptive: `UserNotFoundError`, `InvalidOrderStatusError`
- Use cases never throw raw `Error` — always a typed domain error
- Error codes are stable strings (used by adapters to map to HTTP/gRPC status)

### Validation
- Input validation happens at the use case boundary, not in entities
- [Specify: Zod / class-validator / manual guards — pick one and name it here]
- Entities enforce invariants via methods, not constructor guards

## Naming conventions

| Concept            | Convention                        | Example                    |
|--------------------|-----------------------------------|----------------------------|
| Entity             | PascalCase noun                   | `Order`, `Invoice`         |
| Repository iface   | `I[Entity]Repository`             | `IOrderRepository`         |
| Use case class     | `[Verb][Noun]UseCase`             | `CreateOrderUseCase`       |
| Use case iface     | `I[Verb][Noun]UseCase`            | `ICreateOrderUseCase`      |
| Input DTO          | `[Verb][Noun]InputDto`            | `CreateOrderInputDto`      |
| Read DTO           | `[Entity]Dto`                     | `OrderDto`                 |
| Domain error       | `[Noun][Adjective/Verb]Error`     | `OrderNotFoundError`       |
| DI token           | `[DOMAIN]_[ROLE]` (SCREAMING)     | `ORDER_REPOSITORY`         |

## What belongs in core

- Entities and their domain methods
- Repository interfaces (not implementations)
- Use case interfaces and implementations
- DTOs (input + output shapes)
- Domain errors
- DI tokens (`tokens.ts`)
- Shared value objects (e.g. `Money`, `Address`)
- Domain services (stateless logic used by multiple use cases)

## What does NOT belong in core

- Database queries or ORM models
- HTTP handlers, middleware, route definitions
- Email/SMS/push notification sending
- File uploads or storage
- Authentication token generation (auth logic is a use case; JWT signing is infrastructure)
- Environment config or secrets
- Logging implementation (logging interface only, if needed)

## External systems this core is agnostic to

[List: e.g. MongoDB, PostgreSQL, SendGrid, Stripe — core must never know these exist]
```
