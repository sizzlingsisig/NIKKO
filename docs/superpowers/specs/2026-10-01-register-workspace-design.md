# Register Workspace Redesign — Design Spec

**Date:** 2026-10-01
**Status:** awaiting user review
**Path:** architectural (brainstorming → spec → writing-plans)
**Reference:** user-provided mockup (two screenshots, same design) — "redesign content to something like this"

## 1. Intent (user-confirmed)

Redesign the register view's content to match the provided "document workspace"
mockup: a workspace header bar, a horizontal 3-phase strip, a left sidebar of
reference cards, and a framed "docket" panel holding the step content — plus a
stationery page footer. The wizard's logic (upload → parse → review → submit →
acknowledge) is preserved untouched; only its visual frame changes.

This also permanently resolves the half-width dropzone layout bug (root cause:
q-file slot content shrink-wraps inside Quasar's flex `no-wrap` control
container) by giving the dropzone a normal full-width block container.

## 2. Recorded decisions

| # | Decision | Choice |
|---|----------|--------|
| D1 | Scope | Register view + page footer. **Navbar untouched** (no `PORTAL 05`, no status chip). |
| D2 | Wizard reach | **All three steps** re-framed in the new workspace chrome (no visual discontinuity between steps). |
| D3 | Mockup metadata claims | **Honest-wired**: keep the visual lines, ground them in real state/labels (see §7). PRODUCT.md principle 4 ("never imply capabilities the build does not have") governs. |
| D4 | Size limits | Code stays authoritative: `MAX_PDF_BYTES = 10 MB`, `MAX_IMAGE_BYTES = 5 MB`. Panel interpolates from constants. PRD.md/PRODUCT.md lines corrected as a side task (§12). |
| D5 | Implementation approach | **A — Workspace shell + step panels**: new layout components; existing step components (`UploadStep`, `ReviewStep`, `DoneStep`) and all composables reused as-is. |

## 3. Goals / Non-goals

**Goals**
- Faithful recreation of the mockup's layout structure using the existing OKLCH
  token system (no new color world; maroon rules, serif/sans/mono faces already exist).
- Step content isolated per component; sidebar/docket swap per step.
- WCAG AA contrast (measured, not assumed) and keyboard parity with today's step jumping.
- Root-cause fix for the dropzone width bug (and `AttachmentUploader`, same defect).

**Non-goals**
- Navbar changes (D1). Admin view changes (except shared footer).
- No real WASM parser, sessions, file hashing, or FAQ page is being built.
- No change to limit constants (D4), composables, router, or backend.
- No pixel-identity with the mockup's type sizes where they conflict with the
  token type scale; tokens win, proportions are preserved.

## 4. Architecture

```
register.vue  (state, composables, reached(), v-if step chain — unchanged)
└── RegisterWorkspace                [new]  layout shell: bar + strip + grid
    ├── WorkspaceBar                 [new]  DOCUMENT WORKSPACE chip line
    ├── PhaseStrip                   [new]  replaces <q-stepper> visual role
    ├── Sidebar (aside)
    │   ├── StepOverviewCard         [new]  per-step eyebrow/title/copy/status
    │   ├── PrivacyCard              [new]  persistent RA 10173 card
    │   └── GuidelinesCard           [new]  variant per step (§6.3)
    └── DocketPanel                  [new]  frame: header / body / meta / actions
        └── step body → existing UploadStep | ReviewStep | DoneStep
```

- New components co-locate under `frontend/src/pages/register/components/`
  (existing convention for step components).
- `<q-stepper>` usage and its deep-restyle block in `register.vue` are deleted;
  step guards keep calling the existing `reached()`.
- Step components currently wrapped in `AppCard` headers lose that frame — the
  DocketPanel header supersedes it; step components render inner content only.
  (Exact wrapper location confirmed during implementation; behavior unchanged.)
- `Form5Dropzone` and `ParseLog` live inside the step-1 body; `ParseLog` keeps
  `role="log"`, `aria-live="polite"`, and its reserved `min-height: 150px`.
- `MainLayout.vue`: only the bottom footer is replaced; letterhead untouched.

## 5. Layout & responsive

- **≥900px:** two-column grid — sidebar ≈30% (≈330px at current
  `--measure-max: 1100px`), docket panel fills the rest. Global measure stays
  1100px; widen only if it reads cramped in review.
- **<900px (stacked):** WorkspaceBar → PhaseStrip (compact 3-cell row, fixed
  short labels) → DocketPanel → Sidebar cards. Nothing hidden behind JS.
- WorkspaceBar right meta (`SECURITY: RESTRICTED · COMPLIANCE: RA 10173`)
  wraps below the title on narrow screens.
- Footer stacks: stationery line above the right-hand labels.

## 6. Component specs

### 6.1 PhaseStrip
- `<ol>` of three cells: mono number badge + eyebrow (state) + title (fixed).
- Titles: `UPLOAD YOUR FORM 5`, `VERIFY STUDENT DATA`, `ISSUANCE & CONFIRMATION`.
- Eyebrow by state: active → `ACTIVE PHASE`; done → `PHASE COMPLETE` (defined
  here; not in mockup); pending → per-step flavor label from mockup:
  step 2 `PENDING PARSING`, step 3 `FINAL STAGE`.
- Styling: active cell = white card + heavy maroon bottom rule (mockup);
  done = muted + check mark; pending = muted/transparent.
- Interaction: reachable steps (`reached()`) render as buttons; unreachable
  render as non-buttons with `aria-disabled`. Active carries `aria-current="step"`.

### 6.2 Sidebar
- **StepOverviewCard:** eyebrow `— STEP 0N / OVERVIEW`, serif headline, body
  copy (§6.3), status box slot.
- **PrivacyCard (persistent):** lock icon, `RA 10173 PRIVACY GUARANTEE`,
  mockup body copy (true today: no persistence), footer row
  `STORAGE RESIDUE · 0 BYTES RETAINED`.
- Step 1 status box: `PARSER ENGINE` label + `FORM5-PARSER · SIM v1.8.4` +
  pill wired to the real parse composable: `● READY` idle / `● PARSING`
  in-flight / `● ERROR` on failure.
- Step 2 status box: field tally (e.g. `FIELDS · 6/6`).
- Step 3 status box: reference ID (echoes panel header).

### 6.3 Per-step copy map
| | Step 1 | Step 2 | Step 3 |
|---|---|---|---|
| Headline | Matriculation Verification | Verify Student Data | Issuance & Confirmation |
| Third card | `§ DOCUMENT GUIDELINES` (01 genuine / 02 unmodified / 03 in-person — mockup copy) | `§ REVIEW GUIDELINES` (check names/IDs; attach photo + signature) | `§ WHAT HAPPENS NEXT` (admin dedupe, export, one reference ID) |

Step-1 body copy honesty fix: *"runs client-side inside this browser's
WebAssembly sandbox"* → **"runs entirely inside your browser — your Form 5
never leaves this device"** (true regardless of simulation).

### 6.4 DocketPanel
- Paper card, **2px maroon top rule**, square corners (existing AppCard idiom).
- **Header:** eyebrow `DOCKET FORM 5-A`, serif title, right meta:
  step 1 `MAX SIZE: {{ formatBytes(MAX_PDF_BYTES) }}` (→ `10.0 MB`),
  step 2 field count, step 3 reference ID.
- **Body:** existing step components (§4).
- **Meta footer (left):** `STATIONERY: REV4 · MODE: SIMULATION`
  (replaces mockup's fake `SESSION`/`HASH`, per D3).
- **Actions (right):** secondary `GUIDELINES & FAQ` → real behavior: scrolls to
  and focuses the sidebar guidelines card (no dead button);
  primary = existing per-step action (`CONTINUE TO STEP 02` disabled until
  valid parse, step-2 submit/consent flow unchanged, step-3 finish unchanged).

### 6.5 Form5Dropzone (restyle) + width fix
- Dashed full-width frame: PDF glyph, headline `Drag and drop your official
  Form 5 PDF here`, `or browse from your computer` link (existing accept
  semantics), green `SELECT FORM 5 PDF` button (`--brand-pine-teal`, white text),
  trust row.
- **Root-cause fix:** slot wrapper (`.dropzone__inner`) gets explicit
  `width: 100%` (block flow) inside the q-file container; absolute-positioned
  native overlay behavior retained (click-anywhere + keyboard a11y unchanged).
  Same width fix applies to `AttachmentUploader`'s q-file.
- Trust row honesty: `PORTAL ENCRYPTION VERIFIED` → **`● ON-DEVICE PROCESSING`**;
  rest kept: `STANDARD PDF SPEC 1.4-2.0 / CRS / SAIS STAMP REQUIRED`.
- Existing reject/toast messages and ParseLog behavior unchanged.

### 6.6 Footer (MainLayout, shared register + admin)
- Left: maroon square + `University of the Philippines · Office of Student
  Affairs & Institutional Registrars`; second line folds in the required
  simulation notice: *Frontend prototype, simulation only — no live registration.*
- Right: `DATA PRIVACY MANUAL · SYSTEM TERMS · STATIONERY SPEC 03-A` as
  **plain non-interactive text** (no dead links).
- Replaces the current footer note (which this preserves in spirit, per
  PRODUCT.md's visible-simulation requirement).

## 7. Wording table (D3 — honest-wired)

| Mockup text | Shipped text |
|---|---|
| `UP-F5-WASM v1.8.4` | `FORM5-PARSER · SIM v1.8.4` (status pill from real composable state) |
| "…inside this browser's WebAssembly sandbox" | "runs entirely inside your browser — your Form 5 never leaves this device" |
| `SESSION: REG-2025-08492 · HASH: e3b0c4…` | `MODE: SIMULATION` |
| `PORTAL ENCRYPTION VERIFIED` | `ON-DEVICE PROCESSING` |
| `MAX SIZE: 10.0 MB` | kept — interpolated from `MAX_PDF_BYTES` |
| `SECURITY: RESTRICTED · COMPLIANCE: RA 10173` | kept (stationery posture labels, not capability claims) |
| Navbar `CRS·SAIS CONNECTED` | **not shipped** (navbar out of scope, D1) |

## 8. Accessibility

- Phase strip: `<ol>`, `aria-current="step"`, `aria-disabled` for locked,
  real `<button>` for reachable — keyboard parity with current header-nav.
- **Measured contrast:** pending/muted phase text on cream is the flagged risk;
  any pair < 4.5:1 gets a darker foreground token (token-compatible, no layout impact).
- Preserve: ParseLog `aria-live` + reserved height, keyboard-operable q-file
  dropzone, labelled inputs, focus move on `GUIDELINES & FAQ`.
- Green button (`#004a36` + white) and maroon-on-cream pairs verified by measurement.

## 9. Error handling

Unchanged semantics: wrong-type/oversize toasts (copy already interpolates
constants), ParseLog tone classes, `reached()` guard rejections, disabled
primary until valid parse, step-2 validation/consent gates.

## 10. Verification plan (no test framework in this prototype)

1. `quasar build` + lint pass.
2. Manual checklist on live `:9000`: step transitions + guards, phase-strip
   jumping, dropzone select/oversize/reject paths, ParseLog lines, full submit
   → reference ID, `<900px` stacking, footer on register + admin.
3. Root-cause regression: dropzone spans full panel width (visual + `width:100%`).
4. User screenshot review before sign-off.

## 11. Files touched

**New:** `pages/register/components/`: `RegisterWorkspace.vue`, `WorkspaceBar.vue`,
`PhaseStrip.vue`, `StepOverviewCard.vue`, `PrivacyCard.vue`, `GuidelinesCard.vue`,
`DocketPanel.vue`.
**Modified:** `pages/register.vue` (template → workspace; QStepper + deep styles removed),
`layouts/MainLayout.vue` (footer), `components/Form5Dropzone.vue` (restyle + width fix),
`components/AttachmentUploader.vue` (width fix), step components (drop superseded
AppCard frame), `css/app.scss` (only if a contrast fix needs a token adjustment).

## 12. Side tasks

- Correct PRD.md (lines 40, 140) and PRODUCT.md (line 58) limits to match code:
  PDF 5 MB → **10 MB**, images 2 MB → **5 MB** (D4).
- PRD's oversize toast spec updates to match the code's interpolated message.

## 13. Risks / open implementation details

- Which file wraps step content in `AppCard` (register vs step components) —
  confirmed at implementation time; outcome is the same (panel frame wins).
- Muted-token contrast outcome may slightly darken pending-phase text vs mockup.
- Compact phase-strip labels on very narrow screens may truncate; fixed short
  labels defined in component.
