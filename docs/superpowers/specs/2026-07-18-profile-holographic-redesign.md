# Holographic Dashboard — GitHub Profile Redesign

**Date:** 2026-07-18
**Status:** Design Approved

## Overview

Redesign `github.com/jthiruveedula` GitHub profile README with a holographic/meta
futuristic aesthetic — floating glass panels, iridescent gradients, HUD-style indicators,
and spatial depth effects — while preserving all existing content.

## Constraints

- GitHub Markdown: no JavaScript, no external CSS, inline styles only
- Must use existing external image services (capsule-render, shields.io, stats cards)
- HTML tables and divs with inline CSS for layout
- SVGs and animated GIFs work (contribution snake)

## Color Palette

| Role        | Color     | Hex       | Usage                            |
|-------------|-----------|-----------|----------------------------------|
| Background  | Deep Space| `#0D1117` | Page background (unchanged)      |
| Primary     | Holo Purple| `#7C3AED` | Nav, secondary accents, glow     |
| Secondary   | Neon Cyan | `#00D4FF` | Primary text, active states      |
| Tertiary    | Holo Orange| `#FF6B35` | Highlights, special badges       |
| Text        | Light Gray| `#C9D1D9` | Body text                        |
| Muted       | Gray      | `#8B949E` | Secondary text                   |

## Section Layout (8 sections, ~600 lines)

### 1. Holographic Header
- Capsule Render wave: iridescent gradient `0:#0D1117 → 50:#7C3AED → 100:#00D4FF`
- Typing SVG subtitle with purple text
- HUD-style badge pills (Open to Work, Views, Followers, Repos) using custom
  shields.io with glass borders
- Tagline in glass container with iridescent left border strip
- Optional: Contribution snake GIF wrapped in glass panel

### 2. HUD Status Bar
- Shields.io badges styled as pill-shaped HUD readouts
- Pill style: `background: rgba(color, 0.1); border: 1px solid rgba(color, 0.3);
  border-radius: 20px`
- 4 badges inline: Open to Work (cyan), Views (cyan), Followers (purple), Repos (orange)
- Hover glow effect via `box-shadow`

### 3. Impact Metrics — Glass Cards
- 2x4 grid of KPI cards in a `<table>` or `<div>` grid
- Each card: glass background, colored top border strip (2px), large value,
  small description
- Value colors cycle: Cyan → Purple → Orange → Cyan → …
- Subtle `box-shadow` for depth

### 4. Expertise Matrix — Holographic Table
- Same 8 skill rows as current
- Row background: alternating glass tints
- Status badges: ACTIVE (cyan glow), DEPLOYED (purple glow)
- Gradient column separator

### 5. Featured Projects — Compact Grid
- 4 category sections (Agent Systems, RAG & Knowledge, LLMOps & Eval,
  Data Engineering & Codegen)
- Each project shown as compact glass card:
  - `dual-agent-platform` ↗ (repo link)
  - One-line description
  - 2-3 tech badge pills
- ~80 lines instead of current ~250 — more glanceable

### 6. Career Timeline — Holographic HUD
- ASCII art timeline with monospace font and gradient text colors
- Role entries as glass panels with:
  - Year · Company · Role header with color dot
  - One-line context summary
  - Achievement table (3-5 rows)
  - Tech tags as pills at bottom
- Same content, tighter rendering

### 7. GitHub Analytics — Floating Stats
- Stats/streak/languages cards wrapped in glass containers
- Activity graph with iridescent gradient line
- Container style: same glass recipe, subtle glow

### 8. Connect + Footer
- Social links as holographic pill buttons
- Iridescent gradient wave footer (capsule-render)

## Glass Panel CSS Recipe

```css
background: linear-gradient(135deg, rgba(124,58,237,0.06), rgba(0,212,255,0.06));
border: 1px solid rgba(124,58,237,0.15);
border-radius: 10px;
box-shadow: 0 4px 24px rgba(124,58,237,0.08), inset 0 1px 0 rgba(255,255,255,0.04);
```

Variants use different primary color opacities for alternating sections.

## Section Dividers

Replace `---` with iridescent gradient `<div>`:

```css
background: linear-gradient(90deg, transparent, #7C3AED, #00D4FF, #FF6B35, transparent);
height: 2px;
box-shadow: 0 0 12px rgba(124,58,237,0.2);
```

## Typography

- Section headings: Fira Code monospace (where supported by inline style)
- Body: GitHub default
- Section numbers/indicators: `◈` kept as section marker with gradient text
