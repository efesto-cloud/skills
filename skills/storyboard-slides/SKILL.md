---
name: storyboard-slides
description: Guide a user from blank page to a researched, structured slide outline through interview plus web research, producing a research dossier and slide outline ready to hand off to prepare-slides. Use when the user needs to build a complex presentation but doesn't know where to start, is staring at a blank page, or wants to storyboard/design a deck before writing it.
---

# Storyboard Slides

Pre-production phase for complex presentations. Produces two artifacts the user can review and edit, then hands off to `prepare-slides` → `slides`.

## Workflow

### 1. Intake

Ask once, in a single message: topic, occasion, any existing materials (files or links). Read everything the user provides before moving on.

### 2. Grill (one question per turn, recommend an answer each time)

Walk the decision tree in order. Skip branches already resolved by intake.

1. **Audience** — who is in the room, seniority, what they already know, what they care about
2. **Intent** — the decision to drive, the feeling to leave, the single takeaway in one sentence
3. **Narrative shape** — problem→solution, chronological, compare/contrast, SCQA, or other
4. **Depth & length** — slide count ceiling, time budget, tolerance for detail
5. **Visual posture** — data-dense, minimal, story/imagery-led, technical diagrams

Always offer a recommended answer so the user can accept fast. If intent is still vague after two rounds, stop and surface the ambiguity — do not keep asking.

### 3. Research

Only after audience and intent are resolved. For each key claim the user wants to make, use WebSearch + WebFetch to pull 1–3 sources. Write `research-dossier.md` in the working directory:

```markdown
## Claim: <one-line claim> {#claim-id}
- Source: <URL> — one-line summary
- Pull quote (if useful): "..."
- Confidence: strong | mixed | weak
```

Flag contradictions explicitly. Never invent stats — if research returns nothing, say so and ask the user for source material instead of filling the gap. Ask the user to skim the dossier and mark which claims survive.

### 4. Outline

Write `slide-outline.md` in the format `prepare-slides` consumes:

```markdown
---
audience: ...
intent: ...
narrative: ...
---

# Presentation Title

## Slide 1: <purpose>
- bullet
- bullet (source: dossier#claim-id)

## Slide 2: <purpose>
...
```

One slide per narrative beat. Reference dossier sections by anchor so downstream steps preserve attribution.

### 5. Handoff

Tell the user: "Run `prepare-slides` next with `slide-outline.md` and `research-dossier.md` as inputs."

## Rules

- One grilling question per turn. Always recommend an answer.
- Research only after audience + intent are locked.
- Never fabricate evidence. Missing sources → ask, don't invent.
- Skip any step the user has already resolved in intake.
