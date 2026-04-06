# Design Specifications

This folder contains **design blueprints** and documentation for the core package.

## 📁 Structure

```
specs/
├── README.md (this file)
├── ARCHITECTURE.md           # Birds-eye view of entire domain
├── QUICK_REFERENCE.md        # Quick answers for writing specs
│
├── entities/                 # One file per entity
│   ├── index.md              # Entity index with quick summaries
│   ├── Provino.md
│   ├── ImpresaFunebre.md
│   └── ...
│
├── usecases/                 # One file per use case (or logical group)
│   ├── index.md              # Use case index by domain
│   ├── SearchProvini.md
│   ├── CreateProvino.md
│   └── ...
│
├── plans/                    # Implementation roadmaps (big features)
│   ├── README.md             # Plans index & guide
│   ├── modello-system.md     # Active plan with checkboxes
│   ├── pdf-export.md
│   └── TEMPLATE-PLAN.md
│
├── drafts/                   # Raw notes, meeting notes, TODOs
│   ├── README.md
│   ├── feature-requests.md
│   ├── known-issues.md
│   └── meetings/
│
└── templates/                # Templates for new specs
    ├── TEMPLATE-CONVERSATIONAL.md (recommended)
    ├── TEMPLATE-MINIMAL.md
    └── TEMPLATE.md
```

## 🎯 Purpose

- 📋 **Plan before coding** - Design entities and use cases upfront
- 🗺️ **Execution roadmaps** - Break big features into daily-tickable steps
- 🧭 **Quick reference** - Understand the domain at a glance
- 📝 **Track decisions** - Document why things are designed a certain way
- 🤝 **Team alignment** - Review and approve designs before work begins
- 🔍 **AI-friendly** - Claude can read specs and implement accurately
- 🗂️ **Capture everything** - Drop raw notes in drafts, formalize later

## 🚀 Quick Start

### Understanding the Domain
1. Read [ARCHITECTURE.md](./ARCHITECTURE.md) - Get the full picture in 5 minutes
2. Browse [entities/index.md](./entities/index.md) - See all entities
3. Browse [usecases/index.md](./usecases/index.md) - See all operations
4. Browse [plans/README.md](./plans/README.md) - See what's in progress

### Planning a New Feature
1. Drop rough notes in [drafts/](./drafts/) first
2. When approved, create implementation plan in `plans/your-feature.md`
3. As you work, create formal specs: `entities/YourEntity.md`, `usecases/YourOperation.md`
4. Tick checkboxes in the plan daily as you progress
5. Update index files and ARCHITECTURE.md

### Capturing Ideas
- Meeting notes → `drafts/meetings/`
- Feature requests → `drafts/feature-requests.md`
- Bugs/issues → `drafts/known-issues.md`
- Random ideas → `drafts/idea-name.md`

Don't overthink it - just write and organize later.

## 📊 Status Markers

- 🔵 **Draft** - Initial idea, under discussion
- 🟡 **In Review** - Ready for team feedback
- 🟢 **Approved** - Greenlit for implementation
- ⚪ **Implemented** - Code written, archived for reference

## 🔄 Workflow

```
drafts/          plans/              entities/ + usecases/
  ↓                ↓                       ↓
[Raw Idea] → [Implementation  → [Formal Specs]
              Plan w/          (created during
              Checkboxes]       plan execution)
                 ↓
           Daily Progress
           (tick boxes)
```

**The Journey**:
1. **Capture** idea in drafts/
2. **Plan** with daily-tickable steps in plans/
3. **Execute** plan, create specs as you build
4. **Maintain** ARCHITECTURE.md, mark plan complete

### For Big Features (Weeks of Work)
1. Create `plans/feature-name.md` (use TEMPLATE-PLAN)
2. Break into phases with daily-tickable checkboxes
3. Link to related drafts and specs
4. Tick boxes as you make progress
5. Create entity/use case specs during implementation
6. Mark plan ✅ Complete when done

### For New Entities
1. Create `entities/EntityName.md` (during plan execution)
2. Add entry to `entities/index.md`
3. Link from related entities and plans
4. Update `ARCHITECTURE.md`
5. Mark status: 🔵 → 🟡 → 🟢 → ⚪

### For New Use Cases
1. Create `usecases/OperationName.md` (during plan execution)
2. Add entry to `usecases/index.md`
3. Link to entity specs and plans
4. Mark status: 🔵 → 🟡 → 🟢 → ⚪

### For Raw Notes
1. Drop in `drafts/` immediately
2. Review periodically
3. Promote to plan when ready to execute
4. Archive or delete old notes

## ✍️ Writing Style

We use a **conversational, sentence-based format**. Write like you're explaining to a colleague.

### Use Case Example

```markdown
As an **operator (ADMIN)**, I want to create a new location with a name and address. 
The name must be unique across all locations.

**Input**: `display_name`, `address`
**Returns**: The created location

**Errors**:
- NotLoggedError - Invalid session
- DuplicateNameError - Name already exists
```

**Key principles**:
- Write naturally: "As an [actor], I want to [action]"
- Be implicit: Actor "operator" means `operator_session_id` is implicit
- Use sentences, not tables
- Lists only for errors or special cases

### Entity Example

```markdown
## Provino

**Collection**: `provinos` | **Soft Delete**: ✅

Memorial plate draft with positioned design elements.

### Core Properties

```
_id, nome, cognome, data_nascita, data_decesso, cimitero, 
dimensioni{larghezza_mm, altezza_mm}, elementi[], impresa_id
```

### Relationships

- Each Provino belongs to an [ImpresaFunebre](./ImpresaFunebre.md)
- Each Provino embeds many ElementoProvino
```

**Use markdown links** to reference other entities/use cases.

## 📚 Templates

Pick the one that fits your needs:

- **templates/TEMPLATE-MINIMAL.md** - Quick idea capture (5 minutes)
- **templates/TEMPLATE-CONVERSATIONAL.md** - Standard format (15-30 min)  
- **templates/TEMPLATE.md** - Comprehensive (when you need everything)

## 🎨 Examples

**Entities**:
- [entities/Location.md](./entities/Location.md) - Simple CRUD entity

**Use Cases**:
- [usecases/SearchProvini.md](./usecases/SearchProvini.md) - Complex search with filters

**Drafts**:
- [drafts/feature-requests.md](./drafts/feature-requests.md) - Running feature list
- [drafts/known-issues.md](./drafts/known-issues.md) - Bug tracking

## 💡 Tips

**Be implicit**:
- "operator" actor → `operator_session_id` is required
- "ADMIN role" → permission check needed
- Returns "entity" → `Result<IEntity, ...>`

**Be concise**:
- List core properties only
- Plain English for relationships
- Skip obvious details

**Focus on what matters**:
- Business rules/constraints
- Who can do what
- Error cases
- Performance notes (indexes, population)

**Iterate**:
- Start rough, refine later
- Mark unknowns with `[ ]`
- Update as you learn

## 🔗 Cross-Referencing

Use **markdown links** to connect specs:

```markdown
<!-- Link to entity -->
See [Provino](../entities/Provino.md) entity

<!-- Link to use case -->
Implemented by [SearchProvini](../usecases/SearchProvini.md)

<!-- Link to draft -->
Feature request: [../drafts/feature-requests.md](../drafts/feature-requests.md)
```

## 🛠️ Integration with Skills

These specs work with coding skills in `/.agents/skills/`:

- **entity** - Reads entity spec, creates entity class
- **persistence** - Creates repo/mapper/document from spec
- **usecase** - Creates use case from spec
- **webapp-loader-action** - Wires route to use case

**Tell Claude**: "Read the spec in `specs/entities/Foo.md` and implement the entity"

## 🗂️ Maintenance

**Update regularly**:
- `ARCHITECTURE.md` - When entities/relationships change
- `entities/index.md` - When adding/removing entities
- `usecases/index.md` - When adding/removing operations
- Entity/use case files - When design evolves

**Review periodically**:
- `drafts/` folder - Promote or archive notes
- Feature requests - Prioritize and groom
- Known issues - Fix or deprioritize
- ⚕️ **Run healthcheck** monthly: [HEALTHCHECK.md](./HEALTHCHECK.md) - Verify alignment, clean up drafts, fix dead links

**Don't let specs rot**:
- If code diverges from spec, update the spec
- Mark implemented features as ⚪
- Archive old/obsolete specs in `drafts/archive/`

## ❓ FAQ

**Q: What's the difference between a plan and a spec?**  
A: **Plans** = execution roadmap with checkboxes (how + when to build). **Specs** = design details (what to build). Plans reference specs. You create specs while executing the plan.

**Q: Do I need a spec for every feature?**  
A: No. Simple bug fixes and UI tweaks don't need specs. Use specs for new entities, complex features, or anything with multiple use cases.

**Q: Do I need a plan for every feature?**  
A: Only for big features (multi-week work). Small features (1-2 days) can go straight to specs or just be implemented.

**Q: How detailed should specs be?**  
A: Just enough to start coding confidently. Don't over-specify. You can always add detail later.

**Q: What if the design changes during implementation?**  
A: Update the spec! Keep it in sync with reality. Plans too - adjust phases as you learn.

**Q: Should I delete old specs?**  
A: No, mark them as ⚪ Implemented for reference. If they're truly obsolete, move to `drafts/archive/`.

**Q: Can I use a different format?**  
A: Yes! The templates are suggestions. Use what works for your brain.

## 🎓 Resources

- [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) - Quick answers to common questions
- [ARCHITECTURE.md](./ARCHITECTURE.md) - Full domain overview
- [templates/](./templates/) - Spec templates
- [plans/README.md](./plans/README.md) - Implementation plans guide
- [HEALTHCHECK.md](./HEALTHCHECK.md) - Periodic maintenance checklist

---

**Start here**: Drop notes in `drafts/`, read `ARCHITECTURE.md`, create plan when ready to execute.

## Integration with Skills

These specs work great with the coding skills in `.agents/skills/`:

- **entity** - Reads spec, creates entity class
- **persistence** - Reads spec, creates repo/mapper/document
- **usecase** - Reads spec, creates use case interfaces and implementations
- **webapp-loader-action** - Reads spec, wires route to use case

You can say: "Read the spec in `specs/my-feature.md` and implement the entity" and Claude will follow it.
