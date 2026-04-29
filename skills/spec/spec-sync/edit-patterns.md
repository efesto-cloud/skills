# Edit Patterns

Common spec edits and exactly how to apply them.
Always prefer the minimal edit. Never reformat surrounding content.

---

## Pattern 1 — Add a field to an entity fields table

**When:** A field was added to the entity during implementation.

**Edit:** Insert one row into the fields table. Match column alignment of existing rows.

**Before:**
```markdown
| id         | string   | UUID, immutable after creation |
| customerId | string   | Required, must reference a User |
```

**After:**
```markdown
| id         | string   | UUID, immutable after creation  |
| customerId | string   | Required, must reference a User |
| discount   | number   | Optional, 0–100 (percentage)    |
```

**Also check:** Use case input DTOs that create or update this entity.

---

## Pattern 2 — Remove a field from an entity fields table

**When:** A field was removed or merged into another during implementation.

**Edit:** Delete the row. Then search all use case specs for references to the old
field name in Steps, Input DTO tables, and acceptance criteria — remove or update each.

**Also check:** If the field had its own validation error, remove it from the
entity's Domain errors section and from every use case errors table that listed it.

---

## Pattern 3 — Remove an invariant that no longer holds

**When:** A business rule was relaxed during implementation (e.g. free orders now allowed).

**Edit:** Delete the invariant bullet. Then:
1. Find every use case Step that enforces this invariant — remove or rewrite the step
2. Find every use case Error that corresponds to violating this invariant — remove the row
3. Find every acceptance criteria WHEN/THEN that tests this invariant — remove the line

**Changelog note:** Mark this as a domain decision, not just a code change.
The reason matters for future readers.

---

## Pattern 4 — Add a new error to a use case

**When:** A new failure path was discovered or added during implementation.

**Edit:**
1. Add a row to the use case `## Errors` table
2. Add a corresponding `WHEN [condition] THEN throw [ErrorName]` to `## Acceptance criteria`
3. If the error originates from an entity invariant, also add it to the entity's
   `## Domain errors` section

**Format:**
```markdown
| `NewDomainError` | When [the specific condition that triggers it] |
```

---

## Pattern 5 — Rename an error

**When:** An error class was renamed for clarity during implementation.

**Edit:**
1. Rename in the entity `## Domain errors` section (if present)
2. Rename in every use case `## Errors` table that lists it
3. Rename in every `## Acceptance criteria` WHEN/THEN that references it
4. Rename in `## Repository interface hints` if it appears there (rare)

**Do a search across all spec files** for the old name before closing the edit.

---

## Pattern 6 — Add a step to a use case

**When:** A new action was added to the use case flow (new validation, new I/O call, etc.).

**Edit:** Insert the step at the correct position in the ordered steps list.
Renumber subsequent steps if they are numbered.

Check whether:
- The new step introduces a new error → add to errors table + acceptance criteria
- The new step calls a new repo method → add to repo interface hints
- The new step delegates to a new dependency → add to dependencies table

---

## Pattern 7 — Remove a step from a use case

**When:** A step was eliminated (logic moved to entity, validation removed, etc.).

**Edit:** Delete the step. Then check:
- Does any error in the errors table only exist because of this step? → remove it
- Does any acceptance criterion test only this step? → remove it
- Does any repo hint exist only because of this step? → remove it

---

## Pattern 8 — Change a repo interface hint method signature

**When:** A repository method was renamed or its signature changed during implementation.

**Edit:** Update the hint in the affected use case spec.
Then search all other use case specs for the old method signature and update each.

**Format:**
```markdown
- `IOrderRepository.findByCustomerId(customerId: string): Promise<Order[]>`
```

---

## Pattern 9 — Add content to "Does NOT"

**When:** A concern was explicitly excluded during implementation review.

**Edit:** Add one bullet point to the `## Does NOT` section.

**Format:**
```markdown
- Does not [verb] [object] — [one-clause reason, e.g. "that is handled by NotifyCustomerUseCase"]
```

Never remove existing "Does NOT" bullets unless the concern is now genuinely in scope
(in which case it needs a full use case spec update, not just removing the exclusion).

---

## Pattern 10 — Update a DTO shape

**When:** Fields were added, removed, or renamed in a DTO during implementation.

**Edit:**
1. Update the DTOs table in the entity spec (fields included column)
2. If it's an input DTO: update the Input section of the relevant use case spec
3. If it's a read DTO: check use case Output sections that reference it

**Note:** If a DTO was split into two DTOs (e.g. `CreateOrderInputDto` split into
`CreateOrderHeaderInputDto` + `CreateOrderItemInputDto`), treat this as a rename
of the original plus an addition of a new DTO — apply Pattern 5 logic plus a new row.

---

## Anti-patterns — never do these during a sync

- **Do not reformat** sections that don't need content changes — it pollutes diffs
- **Do not add "implementation notes"** explaining how the code works — specs describe
  domain intent, not implementation
- **Do not soften language** — keep "must", "shall", "never"; never replace with "should"
- **Do not add Prisma/MongoDB/ORM details** even if that's what changed in the code
- **Do not remove the Changelog section** if it already exists — append only
- **Do not merge two changelog entries** into one — one entry per sync session
