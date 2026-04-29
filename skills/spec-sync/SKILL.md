---
name: spec-sync
description: >
  Keeps spec files in sync with what was actually built. Use this skill whenever the
  user says the spec is out of date, a decision was made during implementation that
  changed the design, a use case or entity was modified, renamed, or removed, or they
  want to reconcile their spec folder against the current codebase. Triggers on phrases
  like "update the spec", "spec is stale", "we changed how X works", "sync the spec",
  "reflect the new design in the spec", "the implementation diverged", "we renamed X",
  "we added a field", "we dropped that use case", or any mention of a gap between the
  spec and the code. Also triggers after a PR or implementation session when the user
  wants to capture what actually got built.
---

# Spec Sync — Hexagonal Core

Updates existing spec files to reflect implementation decisions made after the spec
was written. Produces precise, targeted edits — never rewrites a spec from scratch.
Appends a changelog entry to every file it touches.

---

## Step 0 — Understand the gap before touching anything

Do NOT edit any files immediately. First build a clear picture of what changed and why.

**Extract from context if already provided:**
- Which entities, use cases, or constitution rules changed
- What the old behaviour / design was
- What the new behaviour / design is
- Why the change was made (implementation constraint, new requirement, tech decision)
- Any files or diffs the user has shared

**Ask only for what's still missing** — one consolidated message, max 4 questions:

1. Which spec files are affected? (entity, use case, constitution, or all?)
2. What changed — can you describe the old vs new design, or paste a diff?
3. Was this a domain decision (the business logic changed) or an implementation
   decision (same logic, different tech/structure)?
4. Should the spec reflect the change as a correction (spec was wrong) or as an
   evolution (spec was right, requirements changed)?

The distinction in question 4 matters for how the changelog entry is worded.

---

## Step 1 — Audit the affected specs

Read each affected spec file in full before proposing any edits.

For each file, identify:

- **Stale sections** — content that contradicts the new design
- **Missing content** — new fields, errors, steps, or constraints not yet documented
- **Scope violations** — anything that was added to implementation that shouldn't
  be in the spec (infrastructure details that leaked in, etc.)
- **Cascading effects** — a change in one entity spec may invalidate acceptance
  criteria in a use case spec, or repo interface hints in another use case

> Read `references/staleness-checklist.md` for a section-by-section audit guide.

Summarise the audit findings to the user before making any edits:

```
## Audit findings

### specs/entities/order.md
- ⚠️  Fields table: `discount` field is missing (added during implementation)
- ⚠️  Invariants: rule about minimum total no longer applies (free orders now allowed)

### specs/use-cases/orders/create-order.md
- ⚠️  Step 3: total validation step must be removed
- ⚠️  Errors table: `InvalidOrderError` for zero total should be removed
- ⚠️  Acceptance criteria: WHEN total <= 0 criterion is now incorrect
- ✅  Intent, dependencies, Does NOT — all still accurate

### specs/constitution.md
- ✅  No changes needed
```

Wait for the user to confirm before proceeding to edits.

---

## Step 2 — Apply targeted edits

Edit only the sections that need changing. Never rewrite an entire file.

**Edit rules:**
- Change the minimum number of lines to make the spec accurate
- Preserve wording and structure of sections that are still correct
- When removing content, leave no orphaned references (e.g. if you remove an error
  from the errors table, also remove it from acceptance criteria and steps)
- When adding content, follow the exact format of the surrounding content
- Do not introduce implementation details (no ORM, no HTTP, no framework syntax)
- Do not soften language — keep "must", "shall", "never"; do not replace with "should"

**For each edit, state:**
- Which file and section is being changed
- What the old content was (one-line summary)
- What the new content is
- Why (one sentence referencing the implementation decision)

> Read `references/edit-patterns.md` for common edit patterns and how to apply them.

---

## Step 3 — Check for cascading effects

After applying edits, scan all *other* spec files for content that references
the changed entity, use case, field, or error.

Common cascades to check:

| Changed in...         | May break...                                              |
|-----------------------|-----------------------------------------------------------|
| Entity field removed  | Use case input DTOs, acceptance criteria, repo hints      |
| Error renamed         | Use case errors table, acceptance criteria, entity spec   |
| Use case step changed | Acceptance criteria WHEN/THEN, repo interface hints       |
| Repo method renamed   | All use case specs that reference that repo               |
| Constitution rule     | Every spec file (broad impact — flag, don't auto-fix)     |

Flag any cascading issues found. Fix them if straightforward; flag with ⚠️ if they
need a domain decision before they can be resolved.

---

## Step 4 — Append changelog entries

At the bottom of every file that was modified, append a changelog block.
If the file does not already have a `## Changelog` section, add one.

Format:

```markdown
## Changelog

### [YYYY-MM-DD] — [one-line summary of what changed]
- **Changed:** [section name] — [what was there before → what is there now]
- **Reason:** [implementation constraint / new requirement / tech decision / correction]
- **Cascades resolved:** [list of other files also updated, or "none"]
```

One entry per sync session, even if multiple sections were edited.
Do not collapse multiple separate sync sessions into one entry.

---

## Step 5 — Produce a sync report

After all edits and changelog entries are written, output a final summary:

```
## Sync complete

### Files modified
- specs/entities/order.md — 2 edits
- specs/use-cases/orders/create-order.md — 4 edits

### What changed
- Added `discount` field to Order entity
- Removed zero-total invariant and related error from CreateOrder use case
- Updated 2 acceptance criteria in CreateOrder to reflect free-order allowance

### Cascades resolved
- specs/use-cases/orders/apply-discount.md — updated repo hint method signature

### Still open ⚠️
- specs/constitution.md — if free orders are now a first-class concept, the
  "What belongs in core" section may need a `FreeOrderPolicy` value object.
  Needs a domain decision before speccing.

### Spec integrity
All acceptance criteria in modified files are still in WHEN/THEN format. ✅
No implementation details introduced. ✅
No vague language introduced. ✅
```

---

## Hard rules

- **Never rewrite a spec from scratch** during a sync. If a file is so stale it
  needs a full rewrite, flag it and recommend running `spec-bootstrap` for that
  entity or use case instead.
- **Never remove the "Does NOT" section** from a use case spec, even if everything
  else changes. If its contents need updating, update them — don't delete the section.
- **Never sync in infrastructure details.** If the implementation decision was
  "we switched to Prisma", the spec should NOT mention Prisma. The spec reflects
  the domain contract, not the adapter.
- **Always preserve changelog history.** Append — never overwrite existing entries.
- **If the reason for a change is unclear, ask.** A spec updated without knowing
  why is a spec waiting to drift again.
