---
name: spec-bootstrap
description: >
  Generates a complete spec folder for a hexagonal architecture core package.
  Use this skill whenever the user wants to start writing specs, create a spec folder,
  bootstrap specifications for a new feature or domain entity, or set up spec-driven
  development for a core package. Triggers on phrases like "create specs for", "write
  the spec for", "bootstrap the spec", "set up spec folder", "spec for [entity/use-case]",
  or any mention of wanting documentation-first or spec-driven development for their core.
  Also triggers when the user describes a new entity, use case, or feature and wants to
  capture it as a spec before implementing it.
---

# Spec Bootstrap — Hexagonal Core

Generates the full spec folder structure for a hexagonal architecture `core` package:
one `constitution.md`, plus per-entity and per-use-case spec files.

## Step 0 — Gather context before writing anything

Do NOT start generating files immediately. Extract from conversation history first,
then ask only for what's missing — one message, max 5 questions:

1. What is the domain / package name? (e.g. `billing`, `inventory`, `auth`)
2. List the entities (name + key fields + any known invariants)
3. List the use cases grouped by module (e.g. `orders/CreateOrder`, `orders/CancelOrder`, `invoices/IssueInvoice`)
4. Any non-negotiables for the constitution? (libs, conventions, forbidden imports)
5. Any integrations or external systems the core must remain agnostic to?

Confirm the plan with a short summary before generating.

## Step 1 — Generate `constitution.md`

Read [references/constitution-template.md](references/constitution-template.md) · see [references/examples/constitution-example.md](references/examples/constitution-example.md)

Key sections: Principles · Naming conventions · DI conventions · What belongs/does not belong · Error handling · DTO rules. See [REFERENCE.md](REFERENCE.md) for stack adaptation notes.

## Step 2 — Generate entity specs

Read [references/entity-template.md](references/entity-template.md) · see [references/examples/entity-example.md](references/examples/entity-example.md)

One file per entity: `specs/entities/[entity-name].md`. Each file must begin with frontmatter (`entity`, `status`, `module`). Cover: purpose, fields table, status transitions, invariants, DTOs, domain errors.

## Step 3 — Generate use case specs

Read [references/use-case-template.md](references/use-case-template.md) · see [references/examples/use-case-example.md](references/examples/use-case-example.md)

One file per use case: `specs/use-cases/[module-name]/[use-case-name].md`. Each file must begin with frontmatter (`use-case`, `status`, `module`, `entity`). Group by domain module (e.g. `orders/`, `invoices/`). Cover: intent, dependencies, input/output DTOs, steps, errors table, acceptance criteria, "Does NOT" section.

## Step 4 — Generate index files

Read the four index templates and generate one index file per folder level. Every spec must be reachable from the root index.

- [references/spec-index-template.md](references/spec-index-template.md) → `specs/index.md`
- [references/entities-index-template.md](references/entities-index-template.md) → `specs/entities/index.md`
- [references/use-cases-index-template.md](references/use-cases-index-template.md) → `specs/use-cases/index.md`
- [references/module-index-template.md](references/module-index-template.md) → `specs/use-cases/[module-name]/index.md` (one per module)

`specs/index.md` is the root — it must link to `constitution.md`, `entities/index.md`, `use-cases/index.md`, and each entity/use-case directly. No file should require more than 3 clicks from the root to reach.

## Step 5 — Repository interface hints

Do NOT generate separate repo spec files. Add a `## Repository interface hints` section at the bottom of each use case spec listing the methods it needs. See [REFERENCE.md](REFERENCE.md) for the exact format.

## Step 6 — Output the file tree, then write the files

Show the planned structure first:

```
packages/core/specs/
├── index.md
├── constitution.md
├── entities/
│   ├── index.md
│   └── [entity-name].md
└── use-cases/
    ├── index.md
    └── [module-name]/
        ├── index.md
        └── [use-case-name].md
```

Write each file to disk using the Write tool.

## Step 7 — Flag stubs and open questions

Produce a **"What's still missing"** section:
- ⚠️ Fields or invariants you assumed (user should verify)
- 🔲 Use cases mentioned but not fully specced
- Constitution items that need a decision (e.g. validation library not chosen)

> Quality rules and DTO split guidance: [REFERENCE.md](REFERENCE.md)

## Checklist

- [ ] Constitution covers all sections (principles through external systems)
- [ ] Every entity has a status machine or explicit note that none applies
- [ ] Every entity spec has frontmatter (`entity`, `status`, `module`)
- [ ] Every use case spec has frontmatter (`use-case`, `status`, `module`, `entity`)
- [ ] Every use case has a "Does NOT" section with at least two items
- [ ] Repository interface hints present on every use case spec
- [ ] Every folder in `specs/` has an `index.md` that links to all its direct children
- [ ] `specs/index.md` links to every entity and use case (directly or via sub-index)
- [ ] No unfilled `[placeholders]` remain in any generated file (including index files)
- [ ] "What's still missing" section produced at the end

## Related skills

- `entity` — generates the TypeScript entity class from an entity spec
- `usecase` — generates the use case class + interface + DI binding
- `persistence` — generates the MongoDB repository from repository interface hints
- `population` — generates seed data scripts for the domain
