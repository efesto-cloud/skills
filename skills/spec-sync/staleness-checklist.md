# Staleness Checklist

Section-by-section audit guide. For each section in each spec file type,
check these specific things. Mark ✅ if still accurate, ⚠️ if stale, 🔲 if missing.

---

## constitution.md

| Section                  | Check for                                                        |
|--------------------------|------------------------------------------------------------------|
| Principles / Purity      | Any new forbidden import introduced? Any exception now allowed?  |
| DI conventions           | Token naming pattern changed? New injection style introduced?    |
| Use case contract        | `execute()` signature changed? Return type conventions changed?  |
| DTO rules                | New decorator pattern allowed? New suffix convention?            |
| Error handling           | New base error class? Error code format changed?                 |
| Naming conventions table | Any entity, repo, use case, or error renamed?                    |
| What belongs in core     | New concept added to core that isn't listed?                     |
| What does NOT belong     | Any infrastructure that crept into core during implementation?   |

**Constitution changes are high-impact.** Flag all findings — do not auto-apply.
Constitution changes may cascade to every other spec file.

---

## entities/[entity].md

| Section            | Check for                                                              |
|--------------------|------------------------------------------------------------------------|
| Purpose            | Entity's role in the domain still accurate? Still one sentence?        |
| Fields table       | Fields added, removed, renamed, or type-changed during implementation? |
|                    | Field rules tightened or relaxed (e.g. "required" → "optional")?      |
|                    | New computed or derived fields?                                         |
| Status transitions | New status added? Existing transition removed or guarded differently?  |
|                    | Diagram still matches the rules below it?                              |
| Invariants         | Rule removed (business requirement relaxed)?                           |
|                    | Rule tightened (new constraint discovered)?                            |
|                    | New invariant enforced by a method added during implementation?        |
| DTOs table         | New DTO created? Existing DTO renamed or split? Fields removed?        |
| Domain errors      | Error renamed? New error added? Error moved to a different entity?     |
| Open questions     | Any ⚠️ items now resolved? Remove resolved items, keep unresolved ones.|

---

## use-cases/[use-case].md

| Section                   | Check for                                                          |
|---------------------------|--------------------------------------------------------------------|
| Intent                    | Business goal changed? Still a single sentence?                    |
| Dependencies table        | New repo or service injected? Existing dependency removed?         |
|                           | Token or interface name changed?                                   |
| Input DTO                 | Field added or removed? Field made optional/required?              |
|                           | DTO renamed?                                                       |
| Output DTO                | Return type changed? Now returns void? New fields in output DTO?   |
| Steps                     | Step added, removed, or reordered?                                 |
|                           | Validation logic moved (e.g. from use case to entity method)?      |
|                           | New I/O call added (second repo query, external service)?          |
|                           | Step now delegates to a domain service instead of inline logic?    |
| Errors table              | Error added or removed? Error renamed? Condition changed?          |
| Acceptance criteria       | WHEN/THEN still match the current steps and errors?                |
|                           | Any criterion now always true (can be removed)?                    |
|                           | Any new path not yet covered by a criterion?                       |
| Does NOT                  | Any "does not" now violated by the implementation?                 |
|                           | New adjacent concern excluded that should be documented?           |
| Repository interface hints| Method signature changed? New method needed? Method removed?       |
| Open questions            | Any ⚠️ items resolved? Remove resolved, keep open ones.           |

---

## Cascade lookup table

When a change is found in one file, look up what else may need updating:

| Change type                    | Also check these files / sections                          |
|--------------------------------|------------------------------------------------------------|
| Entity field added             | All use case Input DTOs that create/update this entity     |
|                                | All use case Steps that map or validate this entity        |
|                                | All acceptance criteria referencing this entity's shape    |
| Entity field removed           | Same as above — remove references or flag as missing       |
| Entity field renamed           | All use case specs referencing the old name                |
| Error added to entity          | Use cases that could trigger this error (add to their table)|
| Error renamed                  | Every use case errors table and acceptance criteria        |
| Error removed                  | Every use case that listed it — remove from errors + AC    |
| Use case dependency added      | Constitution "What belongs in core" if it's a new type     |
| Use case input DTO renamed     | Any other spec or doc that references the old name         |
| Repo method signature changed  | All use case specs with repo hints for that method         |
| Use case renamed               | Constitution (if listed), any dependent use case           |
| Use case removed               | Any "Does NOT" that deferred to the removed use case       |
| Constitution naming change     | Every spec file that uses the old naming pattern           |
