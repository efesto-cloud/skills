# Known Issues

Bugs, problems, and technical debt to address.

---

## Critical

### None currently

---

## High Priority

### Compositore - Font Size Calculation
**Date**: 2026-03-15  
**Component**: Client webapp compositore

When changing font family, need to verify that `x_height_ratio` updates correctly and `fontSize_mm` recalculates to maintain visual height.

**Impact**: Text elements may appear wrong size after font change

**Workaround**: Manually adjust font size after changing font

---

### Provino - Date Fields Empty Block Save
**Date**: 2026-02-20  
**Component**: Admin webapp provino edit

When date fields (`data_nascita`, `data_decesso`) are cleared/empty, form validation blocks save even though dates are optional.

**Impact**: Cannot save provino with empty dates

**Workaround**: Keep dates filled

**Fix**: Update validation schema in admin form

---

## Medium Priority

### Impresa - Duplicate Key Error on Counter
**Date**: 2026-01-10  
**Component**: Core - Counter entity

Rare race condition when creating multiple provini for same impresa simultaneously causes duplicate key error on counter.

**Impact**: Occasional 500 error on provino creation

**Workaround**: Retry the operation

**Fix**: Need atomic increment or lock mechanism

---

### Audit Log - No TTL Index
**Date**: 2026-03-01  
**Component**: Core - AuditLog

Audit logs don't have TTL index configured in production. Will fill database over time.

**Impact**: Database bloat

**Fix**: Add TTL index with 90-day expiration (or configurable)

**Status**: Implemented in code, needs migration in production

---

## Low Priority

### Search - Text Index Performance
**Date**: 2026-02-01  
**Component**: Core - Provino search

Text index on `nome`, `cognome`, `cimitero` can be slow with large datasets (10k+ provini).

**Impact**: Search latency increases with data volume

**Workaround**: None needed yet

**Fix**: Consider dedicated search service (Elasticsearch, Algolia) if becomes problem

---

### File Upload - No Progress Bar
**Date**: 2026-01-15  
**Component**: Admin webapp file upload

Large file uploads (STL, high-res images) don't show progress. User doesn't know if upload is working.

**Impact**: UX issue, users think upload is frozen

**Fix**: Add progress bar to UploadFileModal component

---

## Resolved

### ~~Provino - Coordinate Y Inversion~~ ✅
**Date**: 2025-12-15  
**Resolved**: 2026-01-20

Y coordinates were inverted (top=0 vs bottom=0). Fixed by inverting in repository layer.

---

### ~~Impresa - Reset Password Rate Limiting~~ ✅
**Date**: 2025-12-01  
**Resolved**: 2026-01-05

No rate limiting on password reset. Admin could spam resets. Fixed by adding `reset_at` field and checking cooldown period.

---

## Template

When adding an issue:

```markdown
### Issue Title
**Date**: YYYY-MM-DD
**Component**: Package/Module

Description of the problem.

**Impact**: Who/what is affected

**Workaround**: Temporary fix (if any)

**Fix**: What needs to be done
```

When resolved, move to "Resolved" section with ✅ and resolution date.
