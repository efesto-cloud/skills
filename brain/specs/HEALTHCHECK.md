# Documentation Healthcheck

> **Last Run**: -  
> **Next Review**: -  
> **Frequency**: Monthly or after major feature releases

Periodic maintenance checklist to keep specs aligned with reality.

---

## 1. Implementation ↔ Spec Alignment

### Entities

Check each entity in code exists in specs (and vice versa).

**Process**:
1. List entities in code: `ls src/entity/*.ts`
2. List entities in specs: `ls specs/entities/*.md`
3. Compare lists

**Check**:
- [ ] All code entities have spec files
- [ ] All spec entities exist in code (or are draft/planned)
- [ ] Entity properties in specs match actual implementation
- [ ] Relationships documented correctly
- [ ] Soft delete strategy matches (code vs spec)

**Common Issues**:
- Code evolved, specs not updated
- New entity added, no spec created
- Spec says soft delete, code does hard delete (or vice versa)

**Fix**: Update specs or mark as ⚪ Implemented with note "implementation diverged"

---

### Use Cases

Check each use case in code exists in specs.

**Process**:
1. List use cases in code: `find src/useCase -name "*.ts" | grep -v "impl/" | grep ^I`
2. List use cases in specs: `ls specs/usecases/*.md`
3. Compare

**Check**:
- [ ] All implemented use cases have specs (or are in plans)
- [ ] All spec use cases exist in code (or planned)
- [ ] Use case inputs/outputs match implementation
- [ ] Audit decorators mentioned in specs match code

**Common Issues**:
- Quick bug fix added use case, no spec
- Use case inputs changed, spec not updated
- Spec planned but never implemented

**Fix**: Create missing specs or mark specs as 🔵 Draft if not implemented

---

### Repository Methods

Check repo interfaces match implementations.

**Process**:
1. Compare `src/repo/I*Repo.ts` interfaces with `src/repo/impl/*RepoImpl.ts`
2. Check specs mention all key methods

**Check**:
- [ ] Repo interfaces match implementations
- [ ] Major repo methods documented in entity specs
- [ ] Population options correct

**Fix**: Update specs with new methods, remove obsolete ones

---

### Database Reality Check

Check collections and indexes match specs.

**Process**:
1. Look at `ARCHITECTURE.md` database section
2. Compare with MongoDB reality (if accessible)
3. Check code for index definitions

**Check**:
- [ ] Collection names match
- [ ] Key indexes documented
- [ ] TTL indexes noted (audit logs, sessions)

**Fix**: Update `ARCHITECTURE.md` database section

---

## 2. Drafts Cleanup

Review drafts folder for content that can be promoted or archived.

### Feature Requests

**Process**: Read [drafts/feature-requests.md](./drafts/feature-requests.md)

**Check**:
- [ ] ✅ Completed items moved to "Resolved" section or deleted
- [ ] High priority items have plans created
- [ ] Rejected/Won't Do items documented with reason
- [ ] Duplicates merged

**Actions**:
- Move implemented features to resolved
- Create plans for approved features
- Archive old rejected ideas

---

### Known Issues

**Process**: Read [drafts/known-issues.md](./drafts/known-issues.md)

**Check**:
- [ ] Fixed issues moved to "Resolved" section
- [ ] Critical issues properly prioritized
- [ ] Workarounds documented
- [ ] Old issues re-evaluated (still relevant?)

**Actions**:
- Mark resolved issues with ✅ and date
- Delete ancient resolved issues
- Update priority as needed

---

### Meeting Notes

**Process**: Browse [drafts/meetings/](./drafts/meetings/)

**Check**:
- [ ] Old meeting notes archived or deleted (keep last 3 months?)
- [ ] Action items from meetings completed or moved to feature requests
- [ ] Decisions captured in formal specs

**Actions**:
- Archive meetings older than X months
- Extract unfinished action items to feature-requests.md

---

### Orphan Draft Files

**Process**: Look for loose files in [drafts/](./drafts/)

**Check**:
- [ ] Random draft files reviewed
- [ ] Promote useful drafts to plans or specs
- [ ] Delete obsolete drafts

---

## 3. Plans Review

Check implementation plans are current.

**Process**: Review [plans/README.md](./plans/README.md) and plan files

**Check**:
- [ ] Completed plans marked ✅ and dated
- [ ] Active plans have recent progress updates
- [ ] Blocked plans documented with blockers
- [ ] Old completed plans archived or deleted
- [ ] Plans link to correct specs

**Questions per plan**:
- Is this plan still active?
- Are checkboxes up to date?
- Should this be marked complete?
- Is there a blocker that needs attention?

**Actions**:
- Mark complete plans as ✅
- Update progress checkboxes
- Archive old plans (move to `plans/archive/` or delete)
- Update blocker status

---

## 4. Index Files Completeness

Check index files match actual files.

### Entities Index

**Process**: Compare [entities/index.md](./entities/index.md) with `ls entities/*.md`

**Check**:
- [ ] All entity files listed in index
- [ ] All index entries have corresponding files
- [ ] Summaries accurate
- [ ] Links work
- [ ] Status markers correct (🔵🟡🟢⚪)

---

### Use Cases Index

**Process**: Compare [usecases/index.md](./usecases/index.md) with `ls usecases/*.md`

**Check**:
- [ ] All use case files listed in index
- [ ] Organized by domain correctly
- [ ] All index entries have corresponding files
- [ ] Status markers correct

---

### Plans Index

**Process**: Check [plans/README.md](./plans/README.md)

**Check**:
- [ ] Active plans listed
- [ ] Completed plans moved to completed section
- [ ] Links work

---

## 5. Dead Links Check

Find and fix broken markdown links.

**Process**: 
1. Scan all .md files for links: `[text](path)`
2. Check each link resolves

**Common patterns**:
- `[Entity](../entities/Entity.md)` - file exists?
- `[UseCase](../usecases/UseCase.md)` - file exists?
- `[spec](./path.md#anchor)` - anchor exists?

**Check**:
- [ ] All entity references link to existing files
- [ ] All use case references link to existing files
- [ ] All draft references valid
- [ ] All plan cross-references valid
- [ ] No broken anchors (e.g., `#section-name`)

**Tools**:
```bash
# Find all markdown links (quick check)
grep -r '\[.*\](.*\.md' specs/

# Check for common typos
grep -r '\.\.entities' specs/  # Missing slash
grep -r 'usecases\.md' specs/  # Wrong pattern
```

**Actions**:
- Fix broken links
- Remove links to deleted files
- Update paths if files moved

---

## 6. ARCHITECTURE.md Review

Check the main overview is current.

**Process**: Read [ARCHITECTURE.md](./ARCHITECTURE.md)

**Check**:
- [ ] All entities listed
- [ ] Entity summaries accurate
- [ ] Relationships correct
- [ ] Type unions up to date
- [ ] Database collections table complete
- [ ] Example code snippets still accurate
- [ ] Links to entity specs work
- [ ] "Last Review" date updated

**Actions**:
- Add missing entities
- Remove obsolete entities
- Update relationships
- Refresh examples
- Update last review date

---

## 7. Status Markers Accuracy

Check status markers match reality.

**Process**: Scan entities and use cases for status markers

**Check**:
- [ ] 🔵 Draft - Actually drafts or should be 🟢/⚪?
- [ ] 🟡 In Review - Still in review or decision made?
- [ ] 🟢 Approved - Started implementation yet?
- [ ] ⚪ Implemented - Actually in production?

**Actions**:
- Update outdated statuses
- Mark implemented specs as ⚪
- Promote approved specs to in-progress or implemented

---

## 8. Template Files Check

Ensure templates are up to date.

**Process**: Review [templates/](./templates/)

**Check**:
- [ ] Templates reflect current best practices
- [ ] Examples in templates are accurate
- [ ] Templates mentioned in README
- [ ] TEMPLATE-PLAN matches actual plan structure

**Actions**:
- Update templates if format evolved
- Add new sections if needed

---

## 9. Cross-Reference Consistency

Check bidirectional links.

**Examples**:
- If `Provino.md` mentions ImpresaFunebre, does `ImpresaFunebre.md` mention Provino?
- If plan mentions entity spec, does entity mention the plan?
- If use case uses entity, does entity list the use case?

**Check**:
- [ ] Entity relationships are bidirectional
- [ ] Use cases listed in entity specs
- [ ] Plans reference specs, specs reference plans

**Actions**:
- Add missing backlinks
- Keep relationships synchronized

---

## 10. Quick Wins

Low-hanging fruit improvements.

**Check**:
- [ ] Fix typos in main files (README, ARCHITECTURE, indexes)
- [ ] Update dates (Last Review, plan start/complete dates)
- [ ] Remove duplicate content
- [ ] Standardize formatting (consistent headers, bullets)
- [ ] Add missing TODOs to drafts/feature-requests.md

---

## Healthcheck Template

Run this monthly (or after major releases):

```markdown
## Healthcheck - YYYY-MM-DD

**Ran by**: [Name]
**Duration**: [X minutes]

### Summary
- Issues found: X
- Issues fixed: X
- Specs updated: X
- Links fixed: X

### Actions Taken
- [ ] Updated ARCHITECTURE.md
- [ ] Cleaned up drafts/feature-requests.md
- [ ] Archived old plans
- [ ] Fixed X broken links
- [ ] Updated entity specs for X, Y, Z

### Found Issues
1. Entity X spec missing (created)
2. Use case Y implemented but no spec (added to plans)
3. Plan Z marked complete
4. Broken links in entity A (fixed)

### Next Review
- Date: YYYY-MM-DD
- Focus: [What to prioritize next time]
```

---

## Automation Ideas (Future)

**Scripts to create**:
- `check-links.sh` - Find all markdown links, check they resolve
- `sync-entities.sh` - Compare src/entity/*.ts with specs/entities/*.md
- `sync-usecases.sh` - Compare src/useCase with specs/usecases/*.md
- `list-divergence.sh` - Report on specs vs implementation gaps

**VS Code extension ideas**:
- Warn on broken links
- Suggest creating spec when entity is created
- Validate status markers

---

## Notes

- **Don't aim for perfection** - Some divergence is okay during active development
- **Focus on high-value alignment** - Core entities and major use cases matter most
- **Update as you go** - It's easier to maintain than to do big cleanups
- **Mark intentional divergence** - If spec and code differ by design, note it

**Healthy documentation** = Easy to navigate, mostly accurate, links work, not too stale.
