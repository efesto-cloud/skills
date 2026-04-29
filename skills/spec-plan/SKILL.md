---
name: spec-plan
description: >
  Creates and maintains implementation plans inside a todo/ folder that tracks the gap
  between the current codebase and the desired spec state. Use this skill whenever the
  user wants to plan implementation work, identify what's missing from the codebase
  compared to the spec, create a todo list for a use case or entity, write a plan for
  a module or cross-cutting refactoring, update task status during implementation, or
  run linting/gap checks on existing plan files. Triggers on phrases like "write a plan
  for", "what do I need to implement", "create a todo for", "plan this use case",
  "what's missing", "track my implementation progress", "update the plan", "mark this
  as done", "lint the plans", or any mention of implementation status, todos, or gaps
  between spec and code.
---

# Spec Plan — Implementation Planning for Hexagonal Core

Creates structured, ephemeral plan files inside `todo/` that track the gap between
current code and the desired spec state. Plans are living documents — updated during
implementation, then deleted when work is complete.

**Important:** Plans are ephemeral. Nothing in a plan file should be the only place
important decisions are recorded. Decisions belong in `specs/`. Plans only track
the path to get there.

---

## Folder structure

```
todo/
├── plan.md                            ← project-level index + cross-cutting refactors
├── entities/
│   ├── plan.md                        ← multi-entity work
│   └── <entity-name>/
│       └── plan.md                    ← single entity changes
└── use-cases/
    ├── plan.md                        ← cross-module work (rare)
    └── <module-name>/                 ← e.g. orders/, invoices/
        ├── plan.md                    ← module-level sequencing
        └── <use-case-name>/
            └── plan.md               ← single use case task list
```

---

## Step 0 — Determine plan scope

Extract from context or ask:

1. What is the scope? (single use case / single entity / module / cross-cutting)
2. Which spec file(s) does this plan target? (get the exact path)
3. What is the current state of the code? (not started / partial / needs refactor)
4. Are there known blockers or prerequisites from other plans?

Map scope → file location:
- Single use case → `todo/use-cases/<module>/<use-case>/plan.md`
- Entity change → `todo/entities/<entity>/plan.md`
- Multiple entities → `todo/entities/plan.md`
- Module sequencing → `todo/use-cases/<module>/plan.md`
- Refactoring / cross-cutting → `todo/plan.md`

---

## Step 1 — Gap analysis

Before writing tasks, identify the gap between spec and code.

Read the target spec file(s). Then either:
- Read the actual source files if available in context or filesystem
- Ask the user to describe current state if code is not accessible

Produce a **gap summary** — not the plan yet, just the delta:

```
## Gap: CreateOrderUseCase

Missing entirely:
- CreateOrderUseCase class does not exist

Partially implemented:
- Order entity exists but missing `discount` field
- IOrderRepository interface exists but missing `findByCustomerId` method

Needs refactor:
- OrderService contains business logic that should move to CreateOrderUseCase
```

Show the gap summary to the user and confirm before writing the plan.

---

## Step 2 — Write the plan file

> Read `references/plan-template.md` for the full frontmatter schema and task format.

**Frontmatter fields** (all required):

```yaml
---
scope: use-case | entity | module | project
status: not-started | in-progress | blocked | done
spec: <path to the spec file this plan targets>
blocked-by: <path to another plan file, or null>
unblocks: <list of plan paths this plan unblocks, or null>
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Task format** — every task must have:
- A checkbox `- [ ]` or `- [x]`
- A short imperative label (verb first)
- A reference to the spec section it satisfies (in parentheses)
- Optional: a `> note:` line for context or decisions made during implementation

```markdown
- [ ] Add `discount` field to Order entity (`specs/entities/order.md#fields`)
- [ ] Add `findByCustomerId` method to IOrderRepository (`specs/use-cases/orders/create-order.md#repository-interface-hints`)
- [x] Create CreateOrderUseCase class skeleton (`specs/use-cases/orders/create-order.md#intent`)
  > note: placed in src/use-cases/orders/ — matches module folder structure
```

**Task grouping** — group tasks under `##` headers:

For use case plans: `## Prerequisites`, `## Entity changes`, `## Use case implementation`, `## Tests`
For entity plans: `## Field changes`, `## Invariant changes`, `## DTO changes`, `## Cascading use case updates`
For module plans: list use cases as `##` sections with their status and link to their plan
For project plan: list active plans as `##` sections with their `status` pulled from frontmatter

---

## Step 3 — Update the project index

After writing any plan file, update `todo/plan.md` to include a reference to the new plan.

The project index is a dashboard — one line per active plan:

```markdown
## Active plans

| Plan | Scope | Status | Blocked by |
|------|-------|--------|------------|
| [Create Order](use-cases/orders/create-order/plan.md) | use-case | in-progress | — |
| [Order entity: add discount](entities/order/plan.md) | entity | done | — |
| [Orders module sequencing](use-cases/orders/plan.md) | module | not-started | entities/order/plan.md |
```

---

## Step 4 — Updating tasks during implementation

When the user says a task is done, blocked, or needs a note:

1. Check the `- [ ]` → `- [x]` for completed tasks
2. Add a `> note:` line under the task if a decision was made
3. Update `updated:` in frontmatter to today's date
4. Update `status:` in frontmatter if overall plan status changed
5. Re-run the linter: `python scripts/lint_plans.py <path-to-plan>`
6. If plan is fully `done`: remind the user to delete the file and remove from index

Never leave a completed plan file in place. Done means deleted.

---

## Step 5 — Linting and maintenance

Run linting at any time:

```bash
# Lint all plans
python scripts/lint_plans.py

# Lint a specific plan
python scripts/lint_plans.py todo/use-cases/orders/create-order/plan.md

# Check for broken spec links across all plans
python scripts/lint_plans.py --check-links

# Show dashboard of all plan statuses
python scripts/plan_status.py
```

> See `scripts/lint_plans.py` and `scripts/plan_status.py` for what each check covers.

---

## Hard rules

- **Plans reference specs — specs never reference plans.** The spec is timeless; the plan is not.
- **No decisions in plans.** If a decision was made during implementation, it goes in the spec (via spec-sync) or the constitution. The plan's `> note:` is a breadcrumb, not a record.
- **One plan per scope unit.** Don't create a use-case plan that also covers entity changes — split them and link with `blocked-by`.
- **Done means deleted.** A completed plan file is noise. Archive nothing — delete.
- **Update `updated:` every session.** Stale `updated:` dates are a linter error.
