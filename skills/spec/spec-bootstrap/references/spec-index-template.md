# Spec Index Template

## Usage
Root navigation file for the entire specs folder.
Generated once per domain. Every spec file must be reachable from here.

---

```markdown
---
type: spec-index
module: [domain-name]
---

# [DomainName] Core — Specs

[Constitution](constitution.md) — core principles, naming conventions, DI rules.

## Entities
→ [Full index](entities/index.md)

- [[EntityName]](entities/[entity-name].md)

## Use Cases
→ [Full index](use-cases/index.md)

### [ModuleName]
- [[UseCaseName]](use-cases/[module-name]/[use-case-name].md)
```
