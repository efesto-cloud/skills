# Implementation Plans

**Purpose**: Bridge the gap between raw drafts and formal specs. One plan per big feature with daily tickable steps.

---

## What Goes Here

**Big features** like:
- Template system (Modello)
- PDF/PNG export
- Search improvements
- Major refactorings
- Multi-entity features

**Each plan includes**:
- Goal & motivation
- Current state → Target state
- Phases with checkboxes (tick one step per day)
- Links to related drafts/specs
- Dependencies
- Technical notes (for tricky bits only)

---

## Plans vs Specs vs Drafts

| Type | Purpose | Granularity |
|------|---------|-------------|
| **Draft** | Capture raw ideas | Single thought/meeting |
| **Plan** | Execution roadmap | Big feature (weeks of work) |
| **Spec** | Design details | Single entity or use case |

**Workflow**:
1. Idea captured in [../drafts/](../drafts/)
2. Plan created here when ready to execute
3. During execution, create formal specs in [../entities/](../entities/) or [../usecases/](../usecases/)
4. Tick checkboxes in plan as you progress
5. Mark plan as ✅ Complete when done

---

## Active Plans

<!-- Link to active plan files -->
- [ ] [modello-system.md](./modello-system.md) - Template provino system
- [ ] [pdf-export.md](./pdf-export.md) - Export provini as PDF/PNG

---

## Completed Plans

<!-- Move completed plans here -->
- [x] ~~[impresa-access-control.md](./impresa-access-control.md)~~ - Soft delete & revoke access (✅ 2026-01-15)

---

## Rules

✅ **Do**:
- One plan per big feature
- Break into daily-tickable steps
- Link to drafts & specs
- Update status as you go
- Add code snippets for tricky logic only
- Track blockers and dependencies

❌ **Don't**:
- Write the full implementation
- Include every line of code
- Create plans for tiny features (just do them)
- Let plans get stale (update or archive)

---

## Template

Copy [TEMPLATE-PLAN.md](./TEMPLATE-PLAN.md) to start a new plan.

**Lifecycle**:
1. Create plan when feature is approved
2. Tick checkboxes daily as you make progress
3. Create entity/use case specs during implementation
4. Mark plan ✅ Complete when done
5. Archive or delete after a few months
