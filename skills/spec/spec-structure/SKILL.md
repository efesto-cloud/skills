---
name: spec-structure
description: >
  Reference for the canonical folder structure of specs/ and todo/ in a hexagonal
  architecture monorepo core package. Use this skill whenever there is any question
  about where a spec file or plan file should live, how to name it, what belongs in
  specs vs todo, or how to organise use case modules. Triggers on phrases like "where
  does this spec go", "what's the folder structure", "how do I organise specs", "which
  folder for this plan", "spec structure", "todo structure", or any uncertainty about
  file placement in the spec-driven workflow.
---

# Spec & Todo Structure

Two sibling folders. Different time horizons. Never mixed.

```
packages/core/
├── specs/    ← timeless. desired end state. no "current" or "in progress" language.
└── todo/     ← ephemeral. gap-closure plans. deleted when done.
```

---

## specs/

```
specs/
├── index.md                               ← root nav: links to constitution + all folders
├── constitution.md                        ← non-negotiables for the whole core
│                                            (naming, DI rules, what belongs/doesn't)
├── entities/
│   ├── index.md                           ← table of all entities with status
│   └── <entity-name>.md                   ← one file per entity
│                                            (frontmatter + fields, invariants, DTOs, domain errors)
└── use-cases/
    ├── index.md                           ← links to each module index
    └── <module-name>/                     ← group by domain module (orders/, invoices/)
        ├── index.md                       ← table of use cases in this module
        └── <use-case-name>.md             ← one file per use case
                                             (frontmatter + intent, deps, input/output, steps,
                                              errors, acceptance criteria, does-not, repo hints)
```

**Rules:**
- Specs describe the desired state — no references to current code, todo, or progress
- Entity changes (new field, rename, invariant) → edit the entity spec
- Use case changes → edit the use case spec
- Cross-cutting rules → edit constitution.md
- Specs never reference todo/ files
- Every folder in `specs/` must contain an `index.md` that links to all its direct children
- Every entity spec must have frontmatter: `entity`, `status`, `module`
- Every use case spec must have frontmatter: `use-case`, `status`, `module`, `entity`

---

## todo/

```
todo/
├── plan.md                                ← project index + cross-cutting refactors
│                                            (dashboard table of all active plans)
├── entities/
│   ├── plan.md                            ← multi-entity work
│   └── <entity-name>/
│       └── plan.md                        ← single entity: add field, rename, etc.
└── use-cases/
    ├── plan.md                            ← cross-module work (rare)
    └── <module-name>/                     ← mirrors specs/use-cases/ module folders
        ├── plan.md                        ← module sequencing + shared prerequisites
        └── <use-case-name>/
            └── plan.md                    ← single use case task list
```

**Rules:**
- Plans are ephemeral — created when work starts, **deleted when done**
- Every plan file has YAML frontmatter: `scope`, `status`, `spec`, `blocked-by`, `unblocks`, `created`, `updated`
- Tasks use `- [ ]` / `- [x]` with a reference back to the spec section they satisfy
- Decisions made during implementation go into the spec (via spec-sync), not the plan
- `todo/plan.md` is the index — one row per active plan, updated when child statuses change

---

## Scope → file location cheatsheet

| What changed / needs planning          | File to create or edit                              |
|----------------------------------------|-----------------------------------------------------|
| New entity or entity field change      | `todo/entities/<entity>/plan.md`                    |
| Multiple entities affected             | `todo/entities/plan.md`                             |
| Single use case implementation         | `todo/use-cases/<module>/<use-case>/plan.md`        |
| Sequencing within a module             | `todo/use-cases/<module>/plan.md`                   |
| Cross-module or cross-cutting refactor | `todo/plan.md`                                      |
| Constitution rule change               | `todo/plan.md` (high impact — flag, don't bury)     |

---

## Entity change — cross-feature or foundational?

Entity changes are **prerequisites**, not cross-feature work. They unblock use cases.

```
todo/entities/order/plan.md          ← do this first
  unblocks →
    todo/use-cases/orders/create-order/plan.md
    todo/use-cases/orders/apply-discount/plan.md
```

Use `blocked-by` / `unblocks` frontmatter to make this explicit. Never mix entity
tasks into a use case plan.

---

## What lives where — quick rules

| Content                              | lives in specs/ | lives in todo/ |
|--------------------------------------|-----------------|----------------|
| Entity fields and invariants         | ✅              | ❌             |
| Use case steps and acceptance criteria | ✅            | ❌             |
| Implementation task checklist        | ❌              | ✅             |
| Implementation decisions / notes     | ✅ (via sync)   | breadcrumb only|
| Current implementation status        | ❌              | ✅             |
| Why a design decision was made       | ✅ constitution | ❌             |
| Refactoring backlog                  | ❌              | ✅ todo/plan.md|
