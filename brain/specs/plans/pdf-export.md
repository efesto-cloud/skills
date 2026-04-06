# PDF/PNG Export - Implementation Plan

> **Status**: 🔵 Not Started  
> **Priority**: High  
> **Started**: -  
> **Target**: 2026-06-01  
> **Completed**: -

---

## Goal

Allow operators and imprese to export provini as high-quality PDF or PNG files for printing and client preview.

**Problem**: Currently provini only exist in the compositore UI. No way to generate files for external use (printing, email, archival).

**Success Criteria**:
- [ ] Operator can export provino as PDF from admin
- [ ] Operator can export provino as PNG from admin
- [ ] Impresa can download their provini as PDF/PNG from client app
- [ ] Exported files include all positioned elements (text, images) with correct fonts, colors, transforms
- [ ] PDF is print-ready (CMYK? or high-res RGB)

---

## Current State

**What exists**:
- Provino entity with positioned elementi
- ElementoProvino with transforms (x, y, width, height, rotation)
- Text elements with fontFamily, fontSize_mm, x_height_ratio
- Image elements with file references
- Compositore UI renders provino in Canvas/SVG

**What's missing**:
- Server-side rendering engine
- PDF generation
- PNG generation
- Export use cases
- Admin/client routes for export

**Links**:
- Draft request: [../drafts/feature-requests.md](../drafts/feature-requests.md#export--delivery)
- Related entity: [../entities/Provino.md](../entities/Provino.md)

---

## Target State

**Export system**:
- Use case: `ExportProvinoPDF` (operator or impresa)
- Use case: `ExportProvinoPNG` (operator or impresa)
- Server-side rendering with puppeteer or similar
- Admin route: `GET /api/provini/:id/export.pdf`
- Admin route: `GET /api/provini/:id/export.png`
- Client route: `GET /api/client/provini/:id/export.pdf`
- Downloads file with correct MIME type

**Future enhancements** (not in this plan):
- Email provino to client
- Batch export multiple provini
- Watermark for draft provini

---

## Dependencies

- [ ] Choose rendering library (puppeteer, playwright, sharp+canvas, other?)
- [ ] Decide on page size/DPI (A4? Custom based on dimensioni?)
- [ ] Font files available on server (currently only in browser)
- [ ] Image assets accessible (S3 signed URLs or local)

**Blockers**:
- Need to decide on tech stack before starting

---

## Implementation Phases

### Phase 0: Research & Decision
> **Goal**: Choose tech stack

- [ ] Research options:
  - puppeteer: Chrome headless (heavy but full CSS support)
  - playwright: Similar to puppeteer (cross-browser)
  - sharp + node-canvas: Lighter, manual rendering
  - react-pdf: React → PDF directly
- [ ] Evaluate font rendering (need exact x-height matching)
- [ ] Test POC: Render simple provino with text + image
- [ ] **Decision**: Pick library and document why
- [ ] Add dependency to package.json

**Notes**: Puppeteer likely best for exact CSS rendering match with compositore.

---

### Phase 1: Server-Side Rendering
> **Goal**: Generate HTML from provino data

- [ ] Create rendering template (HTML/CSS)
- [ ] Match compositore styles (fonts, positioning, transforms)
- [ ] Create `ProvinRenderer` service
- [ ] Implement `renderToHtml(provino: Provino): string`
- [ ] Handle text elements with correct fonts, sizes, x-height
- [ ] Handle image elements (fetch from storage, embed or link)
- [ ] Handle rotation transforms (CSS rotate)
- [ ] Handle z-index layering
- [ ] Test: Render provino, verify layout matches compositore

**Technical Notes**:

```typescript
// Font sizing in CSS (must match x-height ratio logic)
const fontSizePx = (fontSize_mm * DPI) / 25.4;
const adjustedSize = fontSizePx / x_height_ratio;
```

---

### Phase 2: PDF Generation
> **Goal**: HTML → PDF conversion

- [ ] Implement PDF generation with puppeteer
- [ ] Set page size based on provino.dimensioni
- [ ] Set DPI (300 for print quality)
- [ ] Create `PdfExportService`
- [ ] Implement `exportToPdf(provino: Provino): Promise<Buffer>`
- [ ] Handle fonts (embed or link)
- [ ] Test: Generate PDF, open in viewer, verify quality

**Technical Notes**:

```typescript
// Puppeteer PDF generation
const browser = await puppeteer.launch();
const page = await browser.newPage();
await page.setContent(html);
const pdf = await page.pdf({
  width: `${provino.dimensioni.larghezza_mm}mm`,
  height: `${provino.dimensioni.altezza_mm}mm`,
  printBackground: true,
});
await browser.close();
```

---

### Phase 3: PNG Generation
> **Goal**: HTML → PNG conversion

- [ ] Implement PNG generation with puppeteer
- [ ] Set viewport size based on provino.dimensioni
- [ ] Set resolution (300 DPI)
- [ ] Create `PngExportService`
- [ ] Implement `exportToPng(provino: Provino): Promise<Buffer>`
- [ ] Test: Generate PNG, verify dimensions and quality

---

### Phase 4: Use Cases & API
> **Goal**: Business logic + routes

- [ ] Create use case spec: `usecases/ExportProvinoPDF.md`
- [ ] Create use case spec: `usecases/ExportProvinoPNG.md`
- [ ] Implement `ExportProvinoPDF` use case (operator)
- [ ] Implement `ExportProvinoPNG` use case (operator)
- [ ] Add audit decorator (verb: "EXPORT", metadata: format)
- [ ] Register in DI
- [ ] Create admin route: `GET /api/provini/:id/export.pdf`
- [ ] Create admin route: `GET /api/provini/:id/export.png`
- [ ] Set correct MIME types and headers
- [ ] Test: Download PDF from admin UI
- [ ] Test: Download PNG from admin UI

---

### Phase 5: Client App Integration
> **Goal**: Impresa can export their provini

- [ ] Create client use cases (with impresa auth)
- [ ] Create client routes: `GET /api/client/provini/:id/export.pdf`
- [ ] Add download buttons to client provini detail page
- [ ] Verify permissions (impresa can only export own provini)
- [ ] Test as impresa user

---

### Phase 6: Polish & Documentation
> **Goal**: Production-ready

- [x] Add export buttons to admin provini detail view
- [ ] Add loading indicators during export
- [ ] Handle errors gracefully (missing fonts, images, etc.)
- [ ] Update `ARCHITECTURE.md`
- [ ] Create use case specs
- [ ] Update `usecases/index.md`
- [ ] Mark plan ✅ Complete

---

## Technical Notes

### Font Handling

Fonts must be available on server:
- Option 1: Bundle fonts in Docker image
- Option 2: Download from S3 on startup
- Option 3: Use system fonts (limited selection)

**Decision**: Bundle common fonts, fallback to system fonts.

### Image Handling

Images need to be accessible:
- Option 1: Presigned S3 URLs (simple but requires internet)
- Option 2: Download to temp, embed as base64 (works offline)

**Decision**: Presigned URLs for now, optimize later.

### Performance

- PDF generation takes 2-5 seconds per provino
- Consider queue/background jobs for batch export
- Cache rendered PDFs? (invalidate on provino update)

---

## Testing Strategy

1. **Simple provino**: Text only, no rotation
2. **Complex provino**: Multiple fonts, images, rotations, overlapping elements
3. **Edge cases**: Empty provino, very large provino, special characters in text
4. **Visual comparison**: Side-by-side with compositore rendering

---

## Risks & Mitigations

**Risk**: Font rendering differs from browser  
**Mitigation**: Use same fonts, test extensively, accept minor differences

**Risk**: Puppeteer heavy (500MB+ Docker image)  
**Mitigation**: Consider lighter alternatives if becomes issue, optimize Docker layers

**Risk**: Export takes too long (>10s)  
**Mitigation**: Move to background job queue (separate plan)

---

## Progress Log

- **2026-04-06**: Plan created, Phase 0 not started

---

## Related Plans

- [email-delivery.md](./email-delivery.md) - Send exported PDFs via email (future)
- [batch-operations.md](./batch-operations.md) - Bulk export (future)
