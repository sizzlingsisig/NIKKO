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
    rounded: "0"
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
  horizontal ruled lines (2px). Shadow is a subordinate signal on a named
  subset of surfaces (The Named-Subset Rule), never a stack.
- Square everything: controls and chrome are cut, not moulded.
- Serif for institutional voice, workhorse sans for work, mono strictly for
  code, data, and measurement — never as costume.
- Tracked small caps (0.06em, uppercase, 700) as the only eyebrow device.
- 8pt line-box rhythm; every line height is a strict multiple of 8px (the 404
  numeral is the one declared exception, and says so).

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

### Artwork is not on this ladder
The dropzone illustration paints a *document*, not this interface, so it carries
its own `--illus-*` register — a different maroon ink included. That register is
listed once, under **The Artwork Rule**; do not promote its values into
`--color-*`, and do not demote them into it.

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

**Institutional Serif:** Libre Caslon Text (700), with Georgia and
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
- **Title** (700 serif, `2.5rem`/40px, `4rem`/64px): page statements and large
  figures. The top of the scale.
- **Fluid title** (`--text-title-fluid` = `clamp(--text-subhead, 7vw,
  --text-title)`): the counterfoil reference number on the receipt. It is the
  only display-*adjacent* size in the system, because there is no display step —
  see The Golden Ratio Rule.
- **Subhead** (700, `1.5rem`/24px, `2.5rem`/40px): card and section titles, the
  letterhead lockup, and primary in-control instructions. `--leading-tight`
  (`2rem`/32px) is its single-line variant, for serif lockups that must not sit
  in a 40px box.
- **Body** (400, `1rem`/16px, `1.5rem`/24px): default text. 16px is a floor —
  it also stops iOS zooming inputs on focus. **Body-strong** is the same
  register at 700.
- **Label / caption** (700, `0.75rem`/12px, `1rem`/16px line box): eyebrows at
  `0.06em` and uppercase; meta at 400, untracked.
- **Code / Data** (400 mono, `0.75rem`/12px): timings, filenames, reference IDs,
  byte counts — anything a machine reported, with `tabular-nums` where digits
  advance.
- **Numeral** (`--text-numeral` = `30vh`, with `--leading-none: 1`): the 404
  glyph alone. It must out-scale `--text-title`, and it must opt out of the
  fixed leading or the line box collapses and pulls the glyphs into the title
  above it. Both conditions are load-bearing.

**Weights are two tokens, not a range.** `--weight-regular: 400` and
`--weight-bold: 700`, because the shipped faces cannot honour more: Plus
Jakarta Sans is variable 200–800, but Libre Caslon Text ships 700-only and JetBrains
Mono 400-only, so a 600 or 800 on the serif or the mono would synthesize or fall
back. `.type-data` is locked to 400 for the same reason.

**Tracking is three tokens.** `--tracking-eyebrow: 0.06em` for tracked caps,
`--tracking-normal: 0` everywhere else, and `--tracking-code: 0.1em` for the one
string a student reads back to an admin — the reference ID, where 0.06em crowds
the glyphs at 40px. Migration snapped seven raw values onto this set: `0.05em`
and `0.08em` (inside the illustration, both visible) plus `0.1em` and `0.02em`
(to `--tracking-eyebrow` and `--tracking-normal`), and three bare `0`s (to
`--tracking-normal`). The reference ID's `0.1em` was briefly snapped to
`--tracking-normal` and then given `--tracking-code` to keep it.

### Type roles
Appearance is declared once, in seven global classes. Each sets **typography
only** — never `color` — because type is surface-independent and colour is not.
The role goes in the template beside the existing BEM class, which keeps
identity and layout there; the scoped rule then overrides what it must.

| Role | Family | Size / leading | Weight | Tracking | Case |
|---|---|---|---|---|---|
| `.type-title` | serif | 40px / 64px | 700 | — | — |
| `.type-subhead` | sans | 24px / 40px | 700 | — | — |
| `.type-body` | sans | 16px / 24px | 400 | — | — |
| `.type-body-strong` | sans | 16px / 24px | 700 | — | — |
| `.type-eyebrow` | sans | 12px / 16px | 700 | 0.06em | uppercase |
| `.type-eyebrow-mono` | mono | 12px / 16px | 700 | 0.06em | uppercase |
| `.type-subhead-serif` | serif | 24px / **32px** | 700 | — | — |
| `.type-meta` | sans | 12px / 16px | 400 | — | — |
| `.type-data` | mono | 12px / 16px | 400 | — | `tabular-nums` |

The last two are family variants: a role whose face differs from its sans
default, for the cases "an eyebrow set in mono" and "a subhead in the serif
voice". Without them those surfaces fall back to hand-written CSS — which is
how two mono eyebrows once shipped at weight 400 while three of their siblings
shipped at 700. `.type-eyebrow-mono` is an eyebrow, not a flavour of
`.type-data`: it is bold, tracked and uppercase, where `.type-data` is the
plain mono-as-evidence register.

`.type-subhead-serif` takes `--leading-tight` (32px), not `.type-subhead`'s
40px. **That difference is deliberate** — serif wants less leading than sans
at the same size — and should not be harmonised.

A hand-written typography rule is an exception and must say why, in a comment
at the rule. The common reasons: `.type-*` is a Quasar global that would lose
the specificity tie, the target is a Quasar internal reached through `:deep()`,
the face would be destroyed by the role's `font-family`, or the weight is
deliberately absent (mono labels stay at 400 — the face ships no bold, so a 700
fakes one). A silent hand-written rule is the failure mode this table exists to
prevent.

`.type-meta` and `.type-data` are defined and have no consumer yet; they exist so
that the register is decided rather than re-spelled when those surfaces arrive.
Global `.type-*` sits at specificity 0-1-0, so a Quasar global that lands later
in the stylesheet wins a tie — that is the intended default-then-override
behaviour, and it is why chips and buttons carry a scoped rule instead.

### Role → allowed colours
Because the roles set no colour, the pairing is enforced here. Ratios are the
ones recorded in `app.scss` and the component comments; a pairing that is not on
this table has not been measured, and The Measured Contrast Rule applies.

| Role | Ink | Where it ships |
|---|---|---|
| `.type-title` | `--color-secondary` | Maroon serif on paper, 10.87:1 |
| `.type-subhead` | `--color-foreground` | Graphite on canvas or surface |
| `.type-body` | `--color-foreground` / `--color-foreground-muted` | Graphite on canvas/surface; on any `*-soft` ground 11.8–12.4:1; inverse on the terminal stock; muted 6.00:1 for the console legend |
| `.type-body-strong` | `--color-foreground` / `--color-stamp-error` / `--color-secondary` / `--color-stamp-pending` | Graphite, or destructive on its tint (5.75:1) or on paper (6.57:1); maroon 10.87:1 for the uploader action; pending-stamp 6.00:1 for a filed filename |
| `.type-eyebrow` | `--color-foreground-muted` / `--color-secondary` | Muted on paper 6.00:1 and on sunken stock 5.30:1; maroon on paper 10.87:1, on its tint 9.51:1 |
| `.type-eyebrow-mono` | `--color-foreground-muted` / `--color-secondary` / `--color-on-primary` / `--color-foreground` | As `.type-eyebrow`; white on pine-teal 10.33:1 for the dropzone CTA; graphite inside the amber-tinted OCR stamp |
| `.type-subhead-serif` | `--color-secondary` / `inherit` | Maroon on paper 10.87:1 for card and docket titles; inherited inside the dialog, whose own ink carries it |
| `.type-meta` | `--color-foreground-muted` | As `.type-eyebrow` |
| `.type-data` | `--color-foreground` / `--color-foreground-muted` | Mono ink on paper 13.69:1, muted for secondary rows |

### Named Rules

**The Golden Ratio Rule.** The scale is anchored at 16px and stepped by φ, but
it **stops at 40px**: 12 · 16 · 24 · 40. There is deliberately no step between
12px and 16px — the two are close enough that an intermediate size buys nothing
and costs a decision. Line boxes are strict multiples of 8 (16/24/32/40/64), so
every element lands on the grid without margin fudging. The 64px rung above the
scale was cut with the display tokens, so nothing reaches display size except
`--text-title-fluid`.

**The Mono-As-Evidence Rule.** Mono is for code, data, and measurement — never
for costume. If the string did not come from a machine, it is not set in mono.

**The Absolute-Size Rule.** Type sizes are absolute, because a relative size is
not on the scale at all: `vh` tracks the viewport, `em` and `%` track the parent's
computed font size, and the scale is authored in `rem` against a fixed 16px root.
So the size is decided in one place and a root-font change cannot silently
restage every heading. Two sanctioned exceptions, and no others: relative units
inside SVG user space, where the SVG's own coordinate system is the denominator
and relative sizing is correct by construction; and `--text-numeral`, the 404
glyph, which is the one optical outlier that must out-scale the top rung.

**The Artwork Rule.** The dropzone illustration paints a *document*, not this
interface, so its values live in their own namespace and are never UI tokens:

| Token | Value | Role in the depicted Form 5 |
|---|---|---|
| `--illus-ink` | `#791c24` | Letterhead ink on the slip |
| `--illus-paper` | `#f8f3ef` | Form header wash |
| `--illus-field` | `#efeae4` | Paper wash, field fill |
| `--illus-rule` | `#e6e0da` | Field rules |
| `--illus-divider` | `#d1cdc7` | Divider rule |
| `--illus-muted` | `#6b6661` | Mono caption on the form |
| `--illus-plate` | `#ffffff` | PDF badge plate **and** the slip's paper body — same white, two jobs |
| `--illus-shadow` | `#1b1c1d` | The `<feDropShadow>` flood colour |

`--illus-ink` is **intentionally lighter** than `--color-secondary` (`#7b1113`):
printed ink on paper is not a UI accent. The two must never be "corrected" into
each other — that would restyle the artwork to match the chrome, and the
difference is the whole reason the namespace exists. `--illus-shadow` is not part
of the elevation ladder; it never sees a card surface. The SVG's three labels are
genuinely smaller than caption and are sized by `--illus-text-xs` (9px, "F-5"),
`--illus-text-sm` (10px, the "PDF" plate) and `--illus-text-md` (11px, the "UP"
stamp), set in scoped CSS because presentation attributes cannot read custom
properties. One deliberate exception inside the art: the plate keeps its
synthesized 700, because that is what renders today and snapping it would be a
second undeclared change.

## Layout

**Spacing:** a 4px base with deliberate gaps — `0.25 · 0.5 · 0.75 · 1 · 1.5 · 2
· 3 · 4` rem. **There is no `--spacing-5` (20px)**; it is intentionally absent
and referencing it invalidates the declaration.

**Container:** `--measure-max: 90rem` (1440px), the prototype's main width.

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
within-group spacing stays tight. That grid is the *type* grid — a different 8px
grid runs the elevation ladder's shadow offsets (see Elevation & Depth). The two
are unrelated axes and neither contradicts the other; both rest on the 4px base.

**Dimensions are not spacing.** A size — a thumbnail's width, a badge's minimum
height, a drop target's floor — is a dimension token (`--size-thumb`,
`--size-ack`, `--size-dropzone`), never a `--spacing-*` step. The spacing scale
stays pure so a rhythm change can never resize a decorative tick.

### Motion
Motion is deliberately scarce. The single authored moment is the full-width
maroon rule snapping under the lockup with the active route claiming its segment
of it; everything else moves only to confirm a state change.

- `--duration-fast: 150ms` — hover, tint, and colour shifts on buttons, chips,
  menu rows, and nav links.
- `--duration-base: 220ms` — structural moves that a pointer is following: the
  claim line, the uploader boundary, the dropzone tint.
- `--duration-slow: 350ms` — reserved, no consumer yet.
- `--ease-out: cubic-bezier(0.16, 1, 0.3, 1)` — the only curve. One curve means
  everything that moves decelerates the same way, which is most of what "feels
  consistent" is.

`prefers-reduced-motion: reduce` collapses every animation and transition to
0.01ms globally. Never suppress it, and never reach for `!important` to keep a
transition alive against it.

### Stacking
There is **no z-index scale in the CSS**, and there should not be until something
needs one. `z-index` appears exactly once in the whole component layer — value
`1`, on the sticky toolbar inside `DocumentPreview`'s scroll container, which is
internal stacking inside one component and not a UI layer. Quasar manages its own
`$z-index-*` and is left alone.

The rule when a layer is genuinely needed: **no arbitrary values.** Stacking is
the same idea as elevation, on a second axis — a thing that is higher up should
also be above — so the ladder is `base: 0`, `raised: 10`, `floating: 20`,
`overlay: 30`. Declare it as custom properties at the moment the first component
actually consumes a step, not before; four tokens with zero users is the dead-
token problem the token layer exists to eliminate.

### Named Rules

**The Skip-Five Rule.** The spacing scale has no 5-step. Use `4px` or `16px`,
never `20px`.

## Elevation & Depth

Hierarchy is carried by **rules, hairlines, and tonal fills**. Shadow is a
*subordinate* signal, rationed to a named subset of surfaces: **nothing lifts
that should read as ruled.** A surface that is ruled — table rows, field
separators, the 2px letterhead rule, receipt and entry lines, chips, inputs — is
flat, and stays flat. A surface that is a piece of *paper on a desk*, or a menu
over one, may lift, and then it lifts on the ladder below.

The ladder is four roles, not a menu of steps to pick from. Choose the role that
matches what the surface *is*, and the value is decided:

| Role | Token | Value |
|---|---|---|
| rest | `--elevation-rest` | `none` |
| raised | `--elevation-raised` | `0 8px 16px oklch(0.2992 0.014 40 / 0.1)` |
| floating | `--elevation-floating` | `0 16px 32px oklch(0.2992 0.014 40 / 0.13)` |
| overlay | `--elevation-overlay` | `0 24px 48px oklch(0.2149 0.016 40 / 0.18)` |
| *(state ring, not elevation)* | `--shadow-focus` | `0 0 0 3px oklch(0.3632 0.0739 167.54 / 0.22)` |

Two things about those values are load-bearing. The shadow is **ink-tinted, not
black**: pure black at these alphas reads as an alpha overlay, while the graphite
hue at low chroma reads as pigment settling into paper — which is the material the
whole system is made of. And the offsets run on **their own 8px grid** (y = 8/16/24,
blur = 2× the offset), which is *not* the type grid described under Layout. Both
grids are true, they measure different things, and a card sitting on a 32px
line-box grid while casting an 8px offset is correct, not contradictory.

`--shadow-focus` is a **state ring, not a rung**, and it is deliberately not
renamed into the ladder. Its measured ratio must never move: it is the
non-text contrast guarantee for focus, and it currently has no consumer, because
the focus indicator that actually ships is a 2px `--color-ring` outline
(10.33:1). If you wire it up, wire it up at that value.

### Named Rules

**The Declare-Once Rule.** Elevation is declared once — a border or a shadow,
never both. A 1px border under a wide soft shadow is the ghost card. When a
surface needs a shadow *and* a focus frame, the frame moves into the shadow
stack rather than becoming a second declaration; `AppCard`'s `:focus-within` does
exactly that.

**The Ruled-Ground Rule.** Depth on paper is a horizontal rule first. The 2px
strong rule closes a block; the 1px hairline divides; nothing lifts that should
read as ruled.

**The Named-Subset Rule.** A shadow is permitted only where it is listed here,
and everywhere else the answer is no lift — `--elevation-rest`, which is what a
ruled surface spells `box-shadow: none`. The named subset is short and it is
closed:

- `AppCard` — the shared slip primitive — carries `--elevation-raised`.
- `.q-card` globally takes `--elevation-raised`; this only reaches Quasar cards
  no renderer has overridden, since scoped rules beat the global.
- The document sheet in `DocumentPreview` carries `--elevation-floating`: paper
  resting on the page, not floating over it. The *window* around it keeps a
  hairline and no shadow.
- `.q-menu` (including QSelect dropdowns) carries `--elevation-floating`.
- `.q-dialog` carries `--elevation-overlay`.
- Reserved for a drag-target or sticky bar, with no consumer today: the sticky
  toolbar rides a hairline and a paper ground, and the dropzone's drag state
  rides `background` + `border-color`.

Everything outside that list stays ruled — table row rules, field separators, the
2px letterhead rule, receipt and entry lines, chips, inputs, and `StatTile`. At
admin-table density a shadow reads as noise, which is why the tile that repeats
most is the one that stays flat.

## Shapes

**Square by default.** Controls, buttons, fields, menus, dialogs, and the cards
themselves are cut, not moulded — `border-radius: 0`. The rounded forms that
remain are functional marks, not softened containers:

- `0` — buttons, inputs, menus, dialogs, dropzones, the cards themselves, and
  the document sheet. This is the default for controls *and* for containers.
- `0.375rem` — `--radius-sm`, the focus ring's corner.
- `0.5rem` — `--radius-md`, the one inset stamp in the OCR dialog.
- `0.875rem` — `--radius-xl`, the **global `.q-card` default only**. Every card
  renderer in the app overrides it to `0`, so nothing in the shipped UI is
  rounded at this step; it survives as the Quasar bridge, not as a shape.
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
- **Corner Style:** `0` — `AppCard` is square-cut, deliberately, and overrides
  the global `.q-card` radius. (`.q-card` itself keeps `0.875rem` for Quasar
  cards outside `AppCard`; those are the only consumers of `--radius-xl`.)
- **Background:** `--color-surface` (paper white).
- **Border:** none at rest. The lift *is* the frame — see Elevation.
- **Elevation:** `--elevation-raised`, declared once. No hairline beneath it; a
  1px border under this shadow is the ghost card.
- **Focus-within:** the hairline moves into the shadow stack
  (`--elevation-raised` plus a 1px ink ring) and the 2px amber outline paints
  outside it, offset by one hairline. That ordering is not cosmetic: the ink
  half used to *be* the card's border, so with the border gone a bare amber
  outline would sit straight on white at 1.73:1 — under the 3:1 WCAG 1.4.11
  floor. The offset is load-bearing too. A border paints *inside* the border
  box; a shadow ring paints *outside* it, and an outline paints after the
  element's own shadows. At `outline-offset: 0` the amber would cover the ink
  ring entirely and the amber's inner edge would again touch white. Starting the
  outline where the ink ends puts the two adjacent, so amber-on-ink is 7.90:1.
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
- **Do** set appearance from the seven `.type-*` roles, and colour from the role
  → colour table, rather than hand-writing a bundle in a scoped block.
- **Do** put machine output (timings, filenames, IDs, byte counts) in mono with
  `tabular-nums`.
- **Do** keep amber under or beside graphite, never alone and never under white.
- **Do** measure contrast before shipping a pairing; AA is the floor, AAA is
  the norm.
- **Do** declare elevation once — border *or* shadow — and pick the ladder role
  that matches what the surface is.
- **Do** write corrective error copy that names the problem and the way out.
- **Do** build hierarchy with rules and whitespace before adding another
  container.

### Don't:
- **Don't** round form controls or buttons; square controls are the language.
- **Don't** use `--spacing-5` (20px) — it does not exist in the scale.
- **Don't** use mono as decoration for anything that is not code, data, or a
  measurement.
- **Don't** add gradients, glass, blur, pills on containers, or a stack of
  shadows. One ladder role per surface, never two.
- **Don't** put a border and a shadow on the same element.
- **Don't** lift a ruled surface to solve a hierarchy problem — a rule will do.
- **Don't** size type in `vh`, `%`, or `em` outside SVG user space, and don't
  reach above the top of the scale to get display type.
- **Don't** reach into `--illus-*` for a UI colour, or "correct" `--illus-ink`
  into `--color-secondary`; the illustration is not this palette.
- **Don't** invent a z-index value; take the next step on the layer ladder, and
  declare the token only when something consumes it.
- **Don't** render state through color alone — pair it with a glyph, icon, or
  label.
- **Don't** hide focus (`outline: none`) or suppress `prefers-reduced-motion`.
- **Don't** raise a border above 1px on cards, list items, callouts, or alerts.
