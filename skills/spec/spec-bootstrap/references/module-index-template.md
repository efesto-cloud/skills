# Module Index Template

## Usage
Index file for a single use-case module folder: `specs/use-cases/<module>/index.md`.
One row per use case. Entity column derived from each use-case file's frontmatter.

---

```markdown
---
type: module-index
module: [module-name]
---

# [ModuleName] Use Cases

| Use Case | Entity | Status |
|----------|--------|--------|
| [[UseCaseName]]([use-case-name].md) | [Entity] | draft |
```
