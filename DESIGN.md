---
name: NIKKO — UP Form 5 Registration Portal
description: University stationery for the web — offset-printed UPV letterhead, not an app bar.
colors:
  canvas: "oklch(0.9756 0.0026 106.45)"
  surface: "oklch(1 0 0)"
  surface-sunken: "oklch(0.9591 0.0074 80.72)"
  surface-brand: "oklch(0.9453 0.0224 164.51)"
  surface-inverse: "oklch(0.2149 0.0085 240.3)"
  graphite: "oklch(0.2992 0.0029 17.32)"
  graphite-muted: "oklch(0.4998 0.0222 255.62)"
  line: "oklch(0.9018 0.0145 84.59)"
  line-control: "oklch(0.6318 0.019 84.59)"
  primary: "oklch(0.3632 0.0739 167.54)"
  primary-hover: "oklch(0.2928 0.0575 170.82)"
  primary-soft: "oklch(0.9453 0.0224 164.51)"
  secondary: "oklch(0.3767 0.1396 26.51)"
  secondary-hover: "oklch(0.3096 0.111 25.62)"
  secondary-soft: "oklch(0.9563 0.0186 21.57)"
  accent: "oklch(0.8277 0.1667 79.6)"
  accent-soft: "oklch(0.9659 0.032 87.29)"
  success: "oklch(0.5264 0.1287 151.79)"
  success-soft: "oklch(0.9545 0.0182 161.12)"
  destructive: "oklch(0.5003 0.1821 29.51)"
  destructive-soft: "oklch(0.9563 0.0186 21.57)"
  info: "oklch(0.5007 0.0674 172.06)"
typography:
  display:
    fontFamily: "Libre Caslon Text, Georgia, Times New Roman, serif"
    fontSize: "4rem"
    fontWeight: 700
    lineHeight: "6.5rem"
  title:
    fontFamily: "Libre Caslon Text, Georgia, Times New Roman, serif"
    fontSize: "2.5rem"
    fontWeight: 700
    lineHeight: "4rem"
  subhead:
    fontFamily: "Plus Jakarta Sans, Arial, sans-serif"
    fontSize: "1.5rem"
    fontWeight: 700
    lineHeight: "2.5rem"
  body:
    fontFamily: "Plus Jakarta Sans, Arial, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: "1.5rem"
  label:
    fontFamily: "Plus Jakarta Sans, Arial, sans-serif"
    fontSize: "0.75rem"
    fontWeight: 700
    lineHeight: "1rem"
    letterSpacing: "0.06em"
  code:
    fontFamily: "JetBrains Mono, Liberation Mono, monospace"
    fontSize: "0.75rem"
    fontWeight: 400
    lineHeight: "1rem"
rounded:
  sm: "0.375rem"
  md: "0.5rem"
  lg: "0.625rem"
  xl: "0.875rem"
  pill: "9999px"
spacing:
  1: "0.25rem"
  2: "0.5rem"
  3: "0.75rem"
  4: "1rem"
  6: "1.5rem"
  8: "2rem"
  12: "3rem"
  16: "4rem"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.surface}"
    typography: "{typography.body}"
    rounded: "0"
    height: "2.75rem"
    padding: "0 16px"
  button-primary-hover:
    backgroundColor: "{colors.primary-hover}"
    textColor: "{colors.surface}"
    rounded: "0"
    height: "2.75rem"
  button-outline:
    backgroundColor: "transparent"
    textColor: "{colors.primary}"
    typography: "{typography.body}"
    rounded: "0"
    height: "2.75rem"
    padding: "0 16px"
  chip:
    backgroundColor: "{colors.secondary-soft}"
    textColor: "{colors.secondary}"
    typography: "{typography.label}"
    rounded: "{rounded.pill}"
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.graphite}"
    rounded: "{rounded.xl}"
    padding: "1.5rem"
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.graphite}"
    typography: "{typography.body}"
    rounded: "0"
    height: "2.75rem"
    padding: "0 12px"
  nav-item-active:
    backgroundColor: "transparent"
    textColor: "{colors.secondary}"
    typography: "{typography.label}"
    rounded: "0"
    padding: "0 8px"
---

# Design System: NIKKO

## Overview

**Creative North Star: "UP Letterhead"**

NIKKO is offset-printed university stationery rendered in a browser. The whole
system argues one thing before a word is read — *this is the official channel*,
not a startup's intake form. It refuses the category default of the generic app
bar: logo left, links right, gradient strip. Instead the header is the
letterhead every official UPV document wears, the body is the form that letter
was clipped to, and the submission is a receipt torn off a counterfoil.

The density is document density. Rules do the dividing work that cards and
shadows do elsewhere, information sits on ruled lines the way it sits in a
ledger, and metadata is printed as correspondence metadata rather than shouted
as badges. Motion is deliberately scarce: the single authored moment is the
full-width maroon rule snapping under the lockup with the active route claiming
its segment of it. Everything else moves only to confirm a state change.

The confirmed visual rejections are the direction's own: no gradients, no glass,
no pills, no shadow-stacked chrome, and nothing that looks like a startup.
Contrast is a hard floor (WCAG AA throughout, AAA where the palette allows),
and privacy claims are *demonstrated* — the parse log names the sensitive blocks
it discards — rather than asserted.

**Key Characteristics:**
- Paper and ink: white ground, maroon rules, graphite text, one amber accent.
- Rules, not elevation, carry hierarchy; borders never exceed 1px except
  horizontal ruled lines (2px).
- Square everything: controls and chrome are cut, not moulded.
- Serif for institutional voice, workhorse sans for work, mono strictly for
  code, data, and measurement — never as costume.
- Tracked small caps (0.06em, uppercase, 700) as the only eyebrow device.
- 8pt line-box rhythm; every line height is a strict multiple of 8px.

## Colors

A paper palette: two institution hues, one flame, and a measured neutral ladder.

### Primary
- **Pine-Teal** (`oklch(0.3632 0.0739 167.54)`): the workhorse brand hue and the
  default focus ring. Carries primary buttons, active states, and the
  `:focus-visible` outline (10.33:1 on white). Its hover is the deeper
  `oklch(0.2928 0.0575 170.82)`; its soft wash `oklch(0.9453 0.0224 164.51)`
  backs selected list rows and brand-tinted surfaces.

### Secondary
- **Dark-Wine** (`oklch(0.3767 0.1396 26.51)`): the institutional maroon, and the
  system's signature. It draws the 2px letterhead rule, the active nav state,
  rubber stamps, the "done" chip, and the document watermark (10.87:1 on paper).
  Hover `oklch(0.3096 0.111 25.62)`, soft tint `oklch(0.9563 0.0186 21.57)` for
  stamp grounds.

### Tertiary
- **Amber-Flame** (`oklch(0.8277 0.1667 79.6)`): the seal-gold accent, and the
  only warm hue. It is rationed — focus hairlines, drag-over tints, the active
  nav segment's gold underline, status highlights. Its soft wash
  `oklch(0.9659 0.032 87.29)` is the paper-lit fill for hover and drag states.
  **Never carries white text** (1.73:1); it always sits under graphite
  (7.90:1).

### Neutral
- **Canvas** (`oklch(0.9756 0.0026 106.45)`): page ground.
- **Surface** (`oklch(1 0 0)`): card and slip paper.
- **Sunken** (`oklch(0.9591 0.0074 80.72)`): table heads, hover fills, stage
  grounds — paper set slightly back.
- **Graphite** (`oklch(0.2992 0.0029 17.32)`): body ink (8.9:1+).
- **Graphite-Muted** (`oklch(0.4998 0.0222 255.62)`): meta, provenance, fine
  print (6.00:1).
- **Line** (`oklch(0.9018 0.0145 84.59)`): decorative dividers only (1.34:1).
- **Line-Control** (`oklch(0.6318 0.019 84.59)`): control boundaries, the
  non-text minimum at 3.48:1.
- **Terminal** (`oklch(0.2149 0.0085 240.3)`): the inverse ground for the parse
  log and code blocks.

### Semantic status
- **Success** `oklch(0.5264 0.1287 151.79)` / soft `…0.9545 0.0182 161.12`
- **Destructive** `oklch(0.5003 0.1821 29.51)` / soft `…0.9563 0.0186 21.57`
- **Info** `oklch(0.5007 0.0674 172.06)`

### Named Rules

**The Measured Contrast Rule.** Every ratio in this system is measured, not
estimated, and four pairings are banned outright: amber background with white
text (1.73:1), honeydew on white (1.16:1), wine on pine (1.05:1), and success
text on success-soft (4.45:1). If a pairing is not on the measured table, do not
ship it.

**The Amber Pairing Rule.** Amber is never allowed to speak alone. Its focus
hairline must sit hard against ink (7.90:1); controls with no ink rule keep the
global teal outline instead (10.33:1). Amber alone on paper is 1.73:1 — never.

**The Rationed Accent Rule.** Amber appears at most a handful of times per
screen: focus, drag, and status. Its rarity is what makes it read as the seal.

## Typography

**Display / Institutional Serif:** Libre Caslon Text (700), with Georgia and
Times New Roman as metric-adjusted local fallbacks.
**Body / Workhorse Sans:** Plus Jakarta Sans (variable 200–800), with Arial
metric-matched.
**Label / Data Mono:** JetBrains Mono (400), with DejaVu Sans Mono /
Liberation Mono.

**Character:** An institutional serif making the pronouncements, a compact
neo-grotesque doing all the work, and a mono reserved strictly for things a
machine produced. The serif never sets a paragraph; the mono never sets prose.

All three are self-hosted (73,776 bytes, latin subset) with `size-adjust`-matched
local fallbacks, so a font swap never reflows a ruled baseline.

### Hierarchy
- **Display** (700, `4rem`/64px, `6.5rem`/104px): hero and icon moments only.
- **Title** (700 serif, `2.5rem`/40px, `4rem`/64px): page statements and large
  figures.
- **Subhead** (700, `1.5rem`/24px, `2.5rem`/40px): card and section titles, the
  letterhead lockup, and primary in-control instructions.
- **Body** (400, `1rem`/16px, `1.5rem`/24px): default text. 16px is a floor —
  it also stops iOS zooming inputs on focus.
- **Label** (700, `0.75rem`/12px, `1rem`/16px, `0.06em`, uppercase): eyebrows,
  table headers, field labels, meta.
- **Code / Data** (400 mono, `0.75rem`/12px): timings, filenames, reference IDs,
  byte counts — anything a machine reported, with `tabular-nums` where digits
  advance.

### Named Rules

**The Golden Ratio Rule.** The scale is anchored at 16px and stepped by φ:
12 · 16 · 24 · 40 · 64. Line boxes are strict multiples of 8 (16/24/40/64/104),
so every element lands on the grid without margin fudging.

**The Mono-As-Evidence Rule.** Mono is for code, data, and measurement — never
for costume. If the string did not come from a machine, it is not set in mono.

## Layout

**Spacing:** a 4px base with deliberate gaps — `0.25 · 0.5 · 0.75 · 1 · 1.5 · 2
· 3 · 4` rem. **There is no `--spacing-5` (20px)**; it is intentionally absent
and referencing it invalidates the declaration.

**Container:** `--measure-max: 68.75rem` (1100px), the prototype's main width.

**Touch:** `--touch-target: 2.75rem` (44px) is the minimum interactive height,
applied to buttons, inputs, menu rows, and dropzones.

**Breakpoints in use:** 640px (letterhead expansion returns), 768px (single-row
card padding, dropzone air), 900px (register wizard's counterfoil rail —
`15rem minmax(0,1fr)`, kept under AppSteps' 30rem container-query threshold),
1024px (full desktop header).

**Responsive behavior:** mobile-first and additive. Below 640px the letterhead's
acronym expansion is hidden first; navigation never collapses because there are
exactly two destinations (Register, Admin), both always visible on the bar. The
wizard starts single-column and gains its left counterfoil rail at 900px. Paired
fields use `repeat(auto-fit, minmax(12rem, 1fr))` to self-collapse.

**Rhythm:** 8pt line boxes throughout; section separation is generous while
within-group spacing stays tight.

### Named Rules

**The Skip-Five Rule.** The spacing scale has no 5-step. Use `4px` or `16px`,
never `20px`.

## Elevation & Depth

The system is **flat by design**. Hierarchy is carried by rules, hairlines, and
tonal fills — not by shadow stacks. The direction explicitly bans
"shadow-stacked chrome," and no element may declare elevation twice: a card gets
either a 1px border or a shadow, never both.

Shadows exist but are rationed to a soft, offset, blurred scale that reads as
paper lifting slightly off a desk:

- **2XS** `0 1px 2px 0 oklch(0 0 0 / 0.05)` — resting slips.
- **XS** `0 1px 3px 0 oklch(0 0 0 / 0.06)` — cards at rest (the default).
- **SM** `0 2px 6px -1px oklch(0 0 0 / 0.07)` — slight lift.
- **MD** `0 4px 12px -2px oklch(0 0 0 / 0.09)` — menus and portals.
- **LG** `0 12px 28px -6px oklch(0 0 0 / 0.12)` — dialogs, the document sheet.
- **Focus** `0 0 0 3px oklch(0.3632 0.0739 167.54 / 0.22)` — focus ring.

### Named Rules

**The Declare-Once Rule.** Elevation is declared once — a border or a shadow,
never both. A 1px border under a wide soft shadow is the ghost card.

**The Ruled-Ground Rule.** Depth on paper is a horizontal rule first. The 2px
strong rule closes a block; the 1px hairline divides; nothing lifts.

## Shapes

**Square by default.** Controls, buttons, fields, menus, and dialogs are cut,
not moulded — `border-radius: 0`. The only rounded forms are paper documents and
chips:

- `0` — buttons, inputs, menus, dialogs, dropzones (the default for controls).
- `0.375rem` — `--radius-sm`, focus rings.
- `0.875rem` — `--radius-xl`, cards and the document sheet (paper corners).
- `9999px` — `--radius-pill`, chips and the linear-progress bar only.

**Borders:** 1px is the default and the ceiling for anything that is not a
horizontal ruled line. The two rule widths are `--border-hairline: 1px` for
dividers and control boundaries, and `--border-rule: 2px` for horizontal ruled
lines and focus outlines only — a 2px four-sided border appears nowhere.

**Perforation:** `1px dashed var(--color-border)` marks the tear-off stub /
counterfoil edge on the confirmation receipt.

**Bans:** no pills on containers, no soft "friendly" radii on form controls, no
border-left/right accents above 1px.

## Components

### Buttons
- **Shape:** square (`0`), minimum height `2.75rem` (44px), `0 16px` padding.
- **Type:** body size (16px), weight 700, no text-transform, no letter-spacing.
- **Primary:** pine-teal fill, white text; hover deepens to
  `oklch(0.2928 0.0575 170.82)`.
- **Outline:** transparent fill, pine-teal text, hairline control border; hover
  borders pine-teal.
- **Amber variant:** amber fill must use graphite text (`--color-on-accent`).

### Inputs / Fields
- **Style:** outlined, **square** control, 16px text (stops iOS zoom), label
  set as 12px/700/uppercase/`0.06em` eyebrow.
- **Rest:** 1px `--color-rule-entry` boundary (3.48:1).
- **Hover:** boundary shifts to pine-teal.
- **Focus:** 2px pine-teal ring.
- **Error:** boundary shifts to destructive; message renders as a stamped chip
  (destructive on its soft tint). Focus outranks error visually.
- **Review fields** collapse to a single ruled bottom line, reserving 2px of
  transparent border so focus never shifts layout.

### Cards / Containers
- **Corner Style:** `0.875rem` (`--radius-xl`).
- **Background:** `--color-surface` (paper white).
- **Border:** 1px `--color-border` on rest; hover inks the border to graphite.
- **Elevation:** `--shadow-xs` — and no border + shadow stacking.
- **Internal Padding:** `1.5rem` (24px) mobile, `2rem` (32px) at 768px+.
- **Header:** a 2px maroon rule under the title band closes the block.

### Navigation
- Two text links (Register, Admin) on the letterhead, set as 12px/700/uppercase
  tracked small caps, understated at rest.
- **Active:** claims its segment of the full-width maroon rule — maroon text,
  bolder weight, and a gold hairline sitting on the rule beneath it. This is
  the system's signature moment.
- The claim bar is measured from `getBoundingClientRect()` and re-armed only
  after fonts settle, so it never slides in from zero on load.

### Chips / Stamps
- **Style:** pill radius, 12px/700/`0.06em` uppercase.
- **Done:** maroon on maroon-soft tint (9.51:1). **Error:** destructive on
  its soft tint. **Pending:** muted graphite.
- Rubber-stamp check marks are square, maroon, and pushed to the end of a ruled
  line.

### Signature Component — The Receipt Line
The vocabulary that makes this system itself: ruled prompt lines (text set
between two hairlines like an entry awaiting ink), the full-width letterhead
rule with a claiming segment, the perforated tear-off stub carrying a
`REG-YYYY-NNNNN` reference ID in mono tabular figures, and the terracotta
watermarked document sheet. New surfaces should be built from these four
before reaching for a card.

## Do's and Don'ts

### Do:
- **Do** use 1px for borders and 2px only for horizontal rules and focus
  outlines.
- **Do** set every line box to a multiple of 8px and every control to at least
  44px tall.
- **Do** put machine output (timings, filenames, IDs, byte counts) in mono with
  `tabular-nums`.
- **Do** keep amber under or beside graphite, never alone and never under white.
- **Do** measure contrast before shipping a pairing; AA is the floor, AAA is
  the norm.
- **Do** declare elevation once — border *or* shadow.
- **Do** write corrective error copy that names the problem and the way out.
- **Do** build hierarchy with rules and whitespace before adding another
  container.

### Don't:
- **Don't** round form controls or buttons; square controls are the language.
- **Don't** use `--spacing-5` (20px) — it does not exist in the scale.
- **Don't** use mono as decoration for anything that is not code, data, or a
  measurement.
- **Don't** add gradients, glass, blur, pills on containers, or stacked shadows.
- **Don't** put a border and a shadow on the same element.
- **Don't** render state through color alone — pair it with a glyph, icon, or
  label.
- **Don't** hide focus (`outline: none`) or suppress `prefers-reduced-motion`.
- **Don't** raise a border above 1px on cards, list items, callouts, or alerts.
