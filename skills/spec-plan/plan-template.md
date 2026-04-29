# Plan File Template

## Frontmatter schema

All fields are required. Use `null` explicitly when a field has no value.

```yaml
---
scope: use-case | entity | module | project
status: not-started | in-progress | blocked | done
spec: specs/use-cases/orders/create-order.md        # path to the target spec file(s)
blocked-by: todo/entities/order/plan.md             # path to blocking plan, or null
unblocks:                                           # list of plans this one unblocks
  - todo/use-cases/orders/create-order/plan.md
  - todo/use-cases/orders/cancel-order/plan.md
created: 2026-04-29
updated: 2026-04-29
---
```

For `module` or `project` scope where multiple specs are targeted:
```yaml
spec:
  - specs/use-cases/orders/create-order.md
  - specs/use-cases/orders/cancel-order.md
```

---

## Use case plan template

```markdown
---
scope: use-case
status: not-started
spec: specs/use-cases/orders/create-order.md
blocked-by: todo/entities/order/plan.md
unblocks: null
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# Plan: Create Order Use Case

## Prerequisites
- [ ] Order entity has all required fields (`specs/entities/order.md#fields`)
- [ ] IOrderRepository interface has `save` and `findById` (`specs/use-cases/orders/create-order.md#repository-interface-hints`)
- [ ] IUserRepository interface has `findById` (`specs/use-cases/orders/create-order.md#repository-interface-hints`)

## Use case implementation
- [ ] Create `CreateOrderUseCase` class in `src/use-cases/orders/` (`specs/use-cases/orders/create-order.md#intent`)
- [ ] Inject `IOrderRepository` and `IUserRepository` via constructor (`specs/use-cases/orders/create-order.md#dependencies`)
- [ ] Implement `execute(input: CreateOrderInputDto): Promise<OrderDto>` (`specs/use-cases/orders/create-order.md#input`)
- [ ] Validate customerId — throw `UserNotFoundError` if user not found (`specs/use-cases/orders/create-order.md#steps`)
- [ ] Validate items array is non-empty — throw `InvalidOrderError` (`specs/use-cases/orders/create-order.md#steps`)
- [ ] Persist via `IOrderRepository.save()` (`specs/use-cases/orders/create-order.md#steps`)
- [ ] Map and return `OrderDto` (`specs/use-cases/orders/create-order.md#output`)
- [ ] Register in DI container with token `CREATE_ORDER_USE_CASE` (`specs/constitution.md#dependency-injection`)

## Tests
- [ ] Unit test: valid input → returns OrderDto
- [ ] Unit test: unknown customerId → throws UserNotFoundError
- [ ] Unit test: empty items → throws InvalidOrderError
- [ ] Unit test: repo throws → propagates as RepositoryError
```

---

## Entity plan template

```markdown
---
scope: entity
status: not-started
spec: specs/entities/order.md
blocked-by: null
unblocks:
  - todo/use-cases/orders/apply-discount/plan.md
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# Plan: Order Entity — Add Discount Field

## Field changes
- [ ] Add `discount` field (number, optional, 0–100) to `Order` entity class (`specs/entities/order.md#fields`)
- [ ] Add `discount` to `OrderDto` (`specs/entities/order.md#dtos`)
- [ ] Add `discount` to `CreateOrderInputDto` as optional field (`specs/entities/order.md#dtos`)

## Invariant changes
- [ ] No invariant changes required for this field

## Cascading use case updates
- [ ] Update `CreateOrderUseCase` to pass through `discount` from input to entity (`specs/use-cases/orders/create-order.md#steps`)
  > note: discount is optional — pass undefined if not provided, do not default to 0
```

---

## Module plan template

```markdown
---
scope: module
status: not-started
spec:
  - specs/use-cases/orders/create-order.md
  - specs/use-cases/orders/cancel-order.md
  - specs/use-cases/orders/update-order-status.md
blocked-by: todo/entities/order/plan.md
unblocks: null
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# Plan: Orders Module

Sequencing and shared dependencies for all order use cases.

## Shared prerequisites
- [ ] `IOrderRepository` interface complete with all methods needed by module use cases
- [ ] `Order` entity state machine implemented and tested in isolation
- [ ] `OrderNotFoundError`, `InvalidOrderStatusError` domain errors declared

## Use cases — implementation order

### 1. CreateOrder
status: not-started
plan: [todo/use-cases/orders/create-order/plan.md](../create-order/plan.md)
> must be first — establishes the entity lifecycle entry point

### 2. UpdateOrderStatus
status: not-started
plan: [todo/use-cases/orders/update-order-status/plan.md](../update-order-status/plan.md)
> depends on CreateOrder being stable; exercises the state machine

### 3. CancelOrder
status: not-started
plan: [todo/use-cases/orders/cancel-order/plan.md](../cancel-order/plan.md)
> depends on state machine transitions being correct
```

---

## Project index template

```markdown
---
scope: project
status: in-progress
spec: null
blocked-by: null
unblocks: null
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# Implementation Plan Index

Dashboard of all active plans. Update status here whenever a child plan's status changes.
Done plans are deleted — remove their row from this table when deleted.

## Active plans

| Plan | Scope | Status | Blocked by |
|------|-------|--------|------------|
| [Order entity: add discount](entities/order/plan.md) | entity | in-progress | — |
| [Orders module](use-cases/orders/plan.md) | module | blocked | entities/order/plan.md |
| [Create Order](use-cases/orders/create-order/plan.md) | use-case | not-started | use-cases/orders/plan.md |

## Cross-cutting refactors

- [ ] Move business logic out of `OrderService` into proper use cases
  > affects: src/services/OrderService.ts → split into CreateOrderUseCase, CancelOrderUseCase
  > spec reference: specs/constitution.md#use-cases
- [ ] Rename all repository classes to match `I[Entity]Repository` convention
  > spec reference: specs/constitution.md#naming-conventions
```
