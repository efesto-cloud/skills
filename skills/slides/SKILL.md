---
name: slides
description: >
  Production skill that turns a slide-outline.md into a finished HTML presentation using reveal.js.
  Always use this skill when the user says "generate the slides", "create the presentation", "build the slides",
  "make the HTML", or "turn the outline into slides" — and especially whenever a slide-outline.md file is present
  and the user wants to produce the actual deck. This skill does NOT gather context or draft content; it assumes
  the outline already exists (produced by /storyboard-slides). Trigger immediately on any slide-generation request
  without waiting for the user to mention reveal.js or HTML explicitly.
---

# Slides

Turn `slide-outline.md` into a finished HTML presentation using the bundled reveal.js assets.

## Preconditions

`slide-outline.md` must already exist. If it doesn't, tell the user to run `/storyboard-slides` first and stop.

## Bundled assets

All assets live next to this skill file. Copy relevant ones alongside the output HTML.

| File | Purpose |
|------|---------|
| `assets/template.html` | Base HTML shell — copy this and fill in slides |
| `assets/reveal.js` | Reveal.js library (local, no CDN) |
| `assets/reveal.css` | Reveal.js core styles |
| `assets/theme.css` | Dark theme; edit CSS custom properties in `:root` for brand colors |
| `assets/custom.css` | Footer and print styles |
| `assets/script.js` | Keyboard/touch navigation and animated counters |

Always copy `reveal.js`, `reveal.css`, `theme.css`, `custom.css`, and `script.js` into the same folder as the output HTML so paths resolve correctly.

## Reference files

Read these on demand — don't load all of them upfront.

| File | When to read |
|------|-------------|
| `references/REVEAL.md` | Always — covers slide HTML structure, fragments, transitions, backgrounds |
| `references/advanced-features.md` | When the outline calls for animations, auto-animate, speaker notes, or complex fragments |
| `references/charts.md` | When any slide contains a chart — critical flex/sizing patterns are here |

## Workflow

1. **Read `slide-outline.md`** — note slide count, types (title, content, two-column, chart, etc.), and any animation/chart requirements.
2. **Read `references/REVEAL.md`** (always).
3. **Read `references/charts.md`** if charts are present; **read `references/advanced-features.md`** if animations or complex fragments are needed.
4. **Copy `assets/template.html`** as the output base. Wire local asset paths (`reveal.js`, `reveal.css`, `theme.css`, `custom.css`, `script.js`) relative to the output file.
5. **Implement slides** section by section, following the outline exactly. Don't invent content not in the outline.
6. **Run `scripts/check-charts.js`** if any charts are present.
7. **Run `scripts/check-overflow.js`** to detect overflow at 1920×1080.
8. Fix any reported issues, then report the output path to the user.

### Output location

Default: same directory as `slide-outline.md`. Ask the user if unclear.

## Layout classes

| Class | Use for |
|-------|---------|
| `title-slide` | Opening and closing slides |
| `content-slide` | Bullet points, text |
| `two-column` | Comparisons, side-by-side content |
| `image-left` / `image-right` | Image paired with text |

Keep to 4–5 bullet points per slide; titles under 60 characters.

## Common patterns

### Animated counter
```html
<div class="metric-value" data-target="99.9">0</div>
<div class="metric-label">% Uptime</div>
```
Animates from 0 to `data-target` when the slide becomes active.

### Code block
```html
<div class="code-block">
  <code>
    <span class="code-keyword">function</span>
    <span class="code-command">greet</span>(name) {
      <span class="code-keyword">return</span>
      <span class="code-string">"Hello"</span>;
    }
  </code>
</div>
```
Syntax classes: `.code-keyword`, `.code-string`, `.code-comment`, `.code-command`, `.code-url`

### Highlight box
```html
<div class="highlight-box">
  <strong>Key insight:</strong> Important information here
</div>
```

### Before / after comparison
```html
<div class="before-after">
  <div class="before-box"><div>Before</div></div>
  <div class="arrow-icon">→</div>
  <div class="after-box"><div>After</div></div>
</div>
```

### Diagram with arrow
```html
<div class="diagram">
  <div class="diagram-box primary">
    <div class="diagram-box-title">Component A</div>
  </div>
  <div class="diagram-arrow"></div>
  <div class="diagram-box secondary">Component B</div>
</div>
```

### Custom CSS animation
```css
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}
.animated { animation: fadeIn 0.4s ease-out both; }
.animated:nth-child(2) { animation-delay: 0.2s; }
```
