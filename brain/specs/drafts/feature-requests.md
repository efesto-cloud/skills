# Feature Requests

Running list of requested features. Move to proper specs when ready to implement.

---

## High Priority

### Modello System
**Date**: 2026-01-15  
**Requested by**: Client

- [ ] Create modello (template provino) with positioned elements
- [ ] Generate provino from modello
- [ ] Duplicate modello
- [ ] Wizard: select modello as first step when creating provino

**Status**: Partially implemented, wizard not done

---

### Provino Duplication
**Date**: 2025-12-10  
**Requested by**: Client

- [x] Duplicate entire provino with all elements
- [ ] Link duplicated provino to original (for tracking)

**Status**: Duplication works, linking not implemented

---

### Export & Delivery
**Date**: 2026-02-20  
**Requested by**: Client

- [ ] Export provino as PDF
- [ ] Export provino as PNG/JPG
- [ ] Generate quote/invoice from provino
- [ ] Email provino preview to client
- [ ] Client approval workflow

**Status**: Not started

**Notes**: Needs rendering engine (probably puppeteer or similar)

---

## Medium Priority

### Bulk Operations
**Date**: 2026-03-01  
**Requested by**: Admin request

- [ ] Bulk upload elementi from CSV
- [ ] Bulk update element prices
- [ ] Bulk assign characteristics to elements

**Status**: Not started

---

### Search Improvements
**Date**: 2026-01-20  
**Requested by**: User feedback

- [ ] Search provini by date range (year only, month+year, full date)
- [x] Search provini by cimitero
- [ ] Save search filters as presets
- [ ] Recent searches dropdown

**Status**: Cemetery search done, others pending

---

### Compositore Enhancements
**Date**: Ongoing

- [ ] Text: verify x_height_ratio updates when font changes
- [ ] Selection: multi-select elements (Shift+click)
- [ ] Alignment: align selected elements (left, center, right, top, middle, bottom)
- [ ] Distribution: distribute selected elements evenly
- [ ] Snap to other elements (not just grid)
- [ ] Ruler/measurements overlay
- [ ] Keyboard shortcuts (Del, Ctrl+D duplicate, Ctrl+Z undo)

**Status**: See TODO.md for detailed tracking

---

## Low Priority / Future

### Impresa Self-Service
**Date**: 2026-02-15

- [ ] Impresa can change own password
- [ ] Impresa can view login session history
- [ ] Impresa forgot password flow (email-based)

**Status**: Not started, admin handles for now

---

### Analytics & Reporting
**Date**: 2026-03-10

- [ ] Dashboard: provini created per month
- [ ] Most used elementi
- [ ] Revenue by impresa
- [ ] Export reports as Excel

**Status**: Not started

---

## Rejected / Won't Do

### Remove Defunto Entity
**Date**: 2026-01-05  
**Decision**: Keep for now, but Provino embeds the data directly

We're not actively using Defunto as a separate entity. Provino has nome, cognome, dates directly. Keeping Defunto entity for potential future use but it's low priority.

---

## Template

When adding a new request:

```markdown
### Feature Name
**Date**: YYYY-MM-DD
**Requested by**: Client/Admin/User

- [ ] Task 1
- [ ] Task 2

**Status**: Not started | Planned | In Progress | Blocked

**Notes**: Additional context
```
