# Register Workspace Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the register view's visual frame to the approved workspace mockup (workspace bar, phase strip, sidebar rail, docket panel) and replace the page footer with the stationery footer — without changing wizard logic, composables, or the navbar.

**Architecture:** Approach A (spec §4): new shell components under `frontend/src/pages/register/components/` compose the layout; existing step components (`UploadStep`, `ReviewStep`, `DoneStep`) render inside a new `DocketPanel` body slot; `register.vue` keeps all state and swaps `<q-stepper>` for `RegisterWorkspace`. The dropzone root-cause fix (spec §6.5) rides along in the restyle.

**Tech Stack:** Quasar 2 / Vue 3 SFC, scoped SCSS on existing OKLCH tokens, oxlint/oxfmt + vue-tsc + `quasar build`. **No test framework exists (spec §10)** — each task's test cycle is `typecheck` + `lint:check`, with behavioral assertions as pinned manual checks against the running dev server (`http://localhost:9000`, already running with HMR).

**Spec:** `docs/superpowers/specs/2026-10-01-register-workspace-design.md` — the plan argues from the spec; executors read both.

## Global Constraints

- **Navbar untouched** (spec D1): `MainLayout` letterhead markup/styles are not modified; only `<footer class="app-footer">` changes.
- **Honesty wording (spec §7)** exact strings: `FORM5-PARSER · SIM v1.8.4`, body copy "runs entirely inside your browser — your Form 5 never leaves this device", `STATIONERY: REV4 · MODE: SIMULATION`, `ON-DEVICE PROCESSING`. Never ship: `UP-F5-WASM`, `WebAssembly sandbox`, `SESSION:`/`HASH:`, `PORTAL ENCRYPTION VERIFIED`, `CRS·SAIS CONNECTED`.
- **Interpolate, never hardcode, sizes**: `formatBytes(MAX_PDF_BYTES)` from `@/domain/validation` + `@/domain/roster` → `"10 MB"`. Same for image limits (`MAX_IMAGE_BYTES` = 5 MB).
- **Tokens only** — no raw hex/colors in components. Existing documented contrast pairs (app.scss:109–115) count as measured; **any new text/background pair must be computed ≥4.5:1** before ship (WCAG AA, PRODUCT.md).
- **Square-cut paper world**: `border-radius: 0`, maroon rules via `--color-rule-strong` / `--color-secondary`, hairlines via `--border-hairline`.
- **No new dependencies** (no npm installs). Scripts: `npm run typecheck`, `npm run lint:check`, `npm run build` (run from `frontend/`).
- **Preserve contracts**: step components' props/emits and composables stay as-is except the three pinned changes in Task 7 (UploadStep loses AppCard, DoneStep loses AppCard, ReviewStep loses its own head; `enterReview` stops auto-advancing).
- **One commit per task**, staging only that task's files.

## Review Focus

Inputs/failures the spec implies but no automated test exercises — each pinned to the task that owns it:

1. **Finished-run strip lock** — after submit (`finished=true`), no phase-strip cell may jump steps (receipt lock, register.vue:43-45). → Task 1 defines the gate; **Task 10** verifies: complete flow, click every cell, no movement.
2. **Dropzone width regression (the original bug)** — dropzone must span the full docket panel width, not content width. → **Task 6** step: visual width check + `width: 100%` present; **Task 10** re-check.
3. **File dialog still opens after restyle** — new CTA/trust-row elements sit inside the q-file slot; clicks must still reach the overlaid native (and Enter on the focused zone must open). → **Task 6** pinned manual step.
4. **a11y regressions** — `aria-current="step"` present; ParseLog `aria-live` still announces during parse; Guidelines click moves focus to the sidebar card. → Task 1 (aria), Task 7 (focus wiring), **Task 10** verifies all three.
5. **Unmeasured color pairs** — any new pair (pending cell text, status pill, trust row, footer) not in app.scss:109–115 must be measured ≥4.5:1. → **Task 1** (pending/done cells), **Task 3** (pill), **Task 6** (trust row), **Task 8** (footer); Task 10 confirms none remain unaccounted.

---

### Task 1: PhaseStrip

**Files:**
- Create: `frontend/src/pages/register/components/PhaseStrip.vue`

**Interfaces:**
- Produces (Task 5 consumes): `PhaseStrip` with props `{ step: number; maxReached: number; finished: boolean }` and emit `jump: [step: number]`.

- [ ] **Step 1: Implement `PhaseStrip.vue`**

Structure (ol > li per phase): mono number badge (`01`/`02`/`03`), eyebrow (state label), title. Pinned data:

```ts
const TITLES = ["UPLOAD YOUR FORM 5", "VERIFY STUDENT DATA", "ISSUANCE & CONFIRMATION"];
const PENDING_EYEBROWS = ["", "PENDING PARSING", "FINAL STAGE"];
// eyebrow(i): i === step → "ACTIVE PHASE"; i < step → "PHASE COMPLETE"; else PENDING_EYEBROWS[i]
// done(i) = i < step; active(i) = i === step
// reachable(i) = !finished && i <= maxReached
```

Semantics: each li's interactive element is a real `<button>` when `reachable(i)` (emits `jump(i)`), otherwise a `<span>` with `aria-disabled="true"`; active element carries `aria-current="step"`; badges are buttons only when reachable. Styling (scoped SCSS, tokens): active cell = `--color-surface` card + heavy bottom rule (`--border-rule solid --color-rule-strong`); done cell = `--color-stamp-bg` / `--color-stamp` pair (the pair currently in register.vue:265-272, which this task's later integration deletes); pending text = `--color-foreground-muted` (documented 6.00:1 on paper); badges/eyebrows mono + `--tracking-eyebrow`; cell borders `--border-hairline solid --color-rule-entry`; `<900px` cells shrink but keep all three visible (short labels above already are the short labels).

- [ ] **Step 2: Verify compile + statics**

Run: `cd frontend && npm run typecheck && npm run lint:check`
Expected: both exit 0.

- [ ] **Step 3: Contrast audit for this task's new pairs**

List every new text/bg pair introduced (pending eyebrow/title on cell bg, active on card, done on stamp tint). Confirm each is in the documented table (app.scss:109–115) or compute ≥4.5:1. Record computed values in the PR/commit message.
Expected: no pair < 4.5:1 (adjust token choice, not layout, if one fails).

- [ ] **Step 4: Commit**

```bash
git add frontend/src/pages/register/components/PhaseStrip.vue
git commit -m "feat(register): PhaseStrip component replacing QStepper's visual role"
```

*(Visual mounting check happens in Task 7/10 — component is not yet used.)*

---

### Task 2: WorkspaceBar

**Files:**
- Create: `frontend/src/pages/register/components/WorkspaceBar.vue`

**Interfaces:**
- Produces (Task 5 consumes): `WorkspaceBar`, no props, no emits, static markup.

- [ ] **Step 1: Implement `WorkspaceBar.vue`**

Static markup, pinned copy: left = bordered mono chip span `DOCUMENT WORKSPACE` + `Official University Enrollment Ingestion Docket`; right = `SECURITY: RESTRICTED · COMPLIANCE: RA 10173` (mono, muted). Token styling: hairline bottom rule separator (`--border-hairline solid --color-rule-entry`), chip border maroon (`--color-secondary`), chip text maroon. Responsive: `<640px` the right meta wraps to its own line under the title (flex-wrap).

- [ ] **Step 2: Verify compile + statics**

Run: `cd frontend && npm run typecheck && npm run lint:check`
Expected: both exit 0.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/pages/register/components/WorkspaceBar.vue
git commit -m "feat(register): WorkspaceBar component (document workspace header line)"
```

---

### Task 3: Sidebar cards (StepOverviewCard, PrivacyCard, GuidelinesCard)

**Files:**
- Create: `frontend/src/pages/register/components/StepOverviewCard.vue`
- Create: `frontend/src/pages/register/components/PrivacyCard.vue`
- Create: `frontend/src/pages/register/components/GuidelinesCard.vue`

**Interfaces:**
- Consumes: none.
- Produces (Task 7 consumes):
  - `StepOverviewCard` — props `{ eyebrow: string; title: string }`, slots `default` (body), `status` (status box). Root element must accept fallthrough attrs (`id`, `tabindex`).
  - `PrivacyCard` — no props; static content.
  - `GuidelinesCard` — props `{ variant: "upload" | "review" | "next" }`; root accepts fallthrough attrs (`id`, `tabindex="-1"` needed for Task 7 focus).

- [ ] **Step 1: Implement the three cards**

`StepOverviewCard`: eyebrow line (`— STEP 01 / OVERVIEW` form — caller passes the full string), serif headline (`--font-serif`, `--text-subhead`), body slot, hairline rule, `status` slot content in a bordered status box (hairline border, mono caption label + value rows). Card ground = `--color-surface`, square corners.

`PrivacyCard` (exact copy): heading `RA 10173 PRIVACY GUARANTEE` with lock glyph (inline SVG, `aria-hidden`); body `In compliance with the Philippine Data Privacy Act of 2012, your Form 5 never leaves this device or transmits to any cloud server. Zero server upload residue.`; hairline rule; footer row `STORAGE RESIDUE` (left, mono muted) · `0 BYTES RETAINED` (right, mono, `--color-foreground`). Left accent: card carries a `--color-secondary` left rule per mockup (`border-left: var(--border-rule) solid var(--color-secondary)`).

`GuidelinesCard`: heading `§ DOCUMENT GUIDELINES` (variant `upload`) / `§ REVIEW GUIDELINES` (`review`) / `§ WHAT HAPPENS NEXT` (`next`); ordered items, each = mono maroon `01 / LABEL` line + body copy:
- `upload` (spec §6.3, mockup copy): `01 / GENUINE DOCUMENT` — Form 5 PDF downloaded directly from university SAIS or CRS student portals. · `02 / UNMODIFIED INTEGRITY` — Files with modified text, altered timestamps, or missing watermarks will fail checksum. · `03 / IN-PERSON REGISTRAR` — If automated parsing fails, visit the Office of the University Registrar counters.
- `review`: `01 / CHECK YOUR ENTRIES` — Confirm student number, name, degree program, college and year level against your Form 5. · `02 / ATTACH REQUIRED FILES` — Upload your 2×2 photo and white-paper signature scan (JPG/PNG). · `03 / CONSENT TO PROCEED` — Tick the RA 10173 consent box; submission requires your agreement.
- `next`: `01 / ONE REFERENCE ID` — Your REG-YYYY-NNNNN ID is the proof of this submission — keep it. · `02 / ADMIN DEDUPE` — Org admins keep the latest submission per student. · `03 / ROSTER EXPORT` — The deduplicated roster is exported as CSV/XLSX.

Items separated by hairline rules; item labels mono uppercase `--tracking-eyebrow`.

- [ ] **Step 2: Verify compile + statics**

Run: `cd frontend && npm run typecheck && npm run lint:check`
Expected: both exit 0.

- [ ] **Step 3: Contrast audit**

New pairs: status-box text, `0 BYTES RETAINED` emphasis, guidelines item labels on card surface. Confirm documented or ≥4.5:1; record values.
Expected: no pair < 4.5:1.

- [ ] **Step 4: Commit**

```bash
git add frontend/src/pages/register/components/StepOverviewCard.vue \
        frontend/src/pages/register/components/PrivacyCard.vue \
        frontend/src/pages/register/components/GuidelinesCard.vue
git commit -m "feat(register): sidebar cards (step overview, privacy guarantee, guidelines)"
```

---

### Task 4: DocketPanel

**Files:**
- Create: `frontend/src/pages/register/components/DocketPanel.vue`

**Interfaces:**
- Produces (Task 7 consumes): `DocketPanel` — props `{ eyebrow?: string }` (default `"DOCKET FORM 5-A"`) and `{ title: string }`; slots `default` (body), `meta` (header right), `actions` (footer right).

- [ ] **Step 1: Implement `DocketPanel.vue`**

Structure: article with top accent `border-top: var(--border-rule) solid var(--color-rule-strong)` (the 2px maroon rule), square corners, `--color-surface` ground, `--border-hairline` on remaining sides.
- Header: eyebrow (mono, uppercase, `--tracking-eyebrow`, muted) → `h2` serif title (`--text-title` scale, `--font-serif`); `meta` slot floated right (mono caption).
- Body: default slot, padded `--spacing-6`/`--spacing-8` (matches current AppCard body rhythm).
- Footer: separated by hairline rule; left = fixed mono muted line `STATIONERY: REV4 · MODE: SIMULATION`; right = `actions` slot. Footer always renders (stationery line is part of the panel, spec §6.4).

- [ ] **Step 2: Verify compile + statics**

Run: `cd frontend && npm run typecheck && npm run lint:check`
Expected: both exit 0.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/pages/register/components/DocketPanel.vue
git commit -m "feat(register): DocketPanel frame (maroon rule, meta footer, action slot)"
```

---

### Task 5: RegisterWorkspace

**Files:**
- Create: `frontend/src/pages/register/components/RegisterWorkspace.vue`

**Interfaces:**
- Consumes: `WorkspaceBar`, `PhaseStrip` (props/emit from Task 1/2).
- Produces (Task 7 consumes): `RegisterWorkspace` — props `{ step: number; maxReached: number; finished: boolean }`, emit `jump: [step: number]` (passed through to PhaseStrip), slots `sidebar` and `panel`.

- [ ] **Step 1: Implement `RegisterWorkspace.vue`**

Template: `<WorkspaceBar />` → `<PhaseStrip v-bind props @jump="emit('jump', $event)" />` → grid row: `<aside class="workspace__sidebar"><slot name="sidebar" /></aside>` + `<section class="workspace__panel"><slot name="panel" /></section>`.
Grid (scoped SCSS): `≥900px` → `grid-template-columns: minmax(0, 30%) minmax(0, 1fr); gap: var(--spacing-6)`; `<900px` → single column with DOM order bar → strip → panel → sidebar. **Panel must come after sidebar in DOM for desktop grid placement, but on mobile the panel must display first** — solve with grid `order` (sidebar `order: 2`, panel `order: 1` under 900px), not duplicate markup. `min-width: 0` on both columns.

- [ ] **Step 2: Verify compile + statics**

Run: `cd frontend && npm run typecheck && npm run lint:check`
Expected: both exit 0.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/pages/register/components/RegisterWorkspace.vue
git commit -m "feat(register): RegisterWorkspace shell (bar + strip + sidebar/panel grid)"
```

---

### Task 6: Form5Dropzone restyle + width fix; AttachmentUploader width fix

**Files:**
- Modify: `frontend/src/components/Form5Dropzone.vue` (template copy + styles)
- Modify: `frontend/src/components/AttachmentUploader.vue` (q-file slot width only)

**Interfaces:**
- Consumes: `MAX_PDF_BYTES` (`@/domain/validation`), `formatBytes` (`@/domain/roster`) — already imported.
- Produces: same `accept`/`reject` emits — no contract change. Validation logic (`offer`, `onAdd`, `nameFocusTarget`) is untouched.

- [ ] **Step 1: Root-cause width fix**

In `Form5Dropzone.vue`, `.dropzone__inner` gains `width: 100%` with a WHY comment: Quasar's `.q-field__control-container` is a nowrap flex row; the slot content is its only in-flow child and shrink-wraps to content on the main axis (the half-width bug — flex stretch only affects the cross axis). The q-file root already has `width: 100%` (line 112); the missing piece is the inner box.
Then open `AttachmentUploader.vue`, locate its q-file slot wrapper, apply the same `width: 100%` + one-line comment (same mechanism).

- [ ] **Step 2: Restyle + copy to mockup (spec §6.5)**

Template changes (keep structure `q-file > .dropzone__inner` and all handlers):
- Lead copy → `Drag and drop your official Form 5 PDF here` (stays the `LABEL_ID` target).
- Alt copy → `or browse from your computer`, styled as a link affordance (underline, `--color-secondary`).
- Remove `.dropzone__note` (superseded by panel header `MAX SIZE` + trust row).
- Add visual CTA: `<span class="dropzone__cta" aria-hidden="true">+ SELECT FORM 5 PDF</span>` — **decorative only** (the whole zone is the control; the overlaid native owns clicks — see Step 3). `--color-primary` bg, white text (documented 10.33:1), mono uppercase, `+` glyph span.
- Add trust row (mono caption, centered): line 1 `● ON-DEVICE PROCESSING` (dot `--color-primary`) ` │ STANDARD PDF SPEC 1.4-2.0`; line 2 `CRS / SAIS STAMP REQUIRED` in `--color-secondary`.

Style changes: frame border becomes uniform **dashed** hairline (`--color-rule-entry`, `--border-hairline` but `dashed`) — the solid maroon head rule goes away inside the panel (the DocketPanel now supplies the maroon rule); keep hover/focus/dnd state rules, keeping `--color-rule-strong` for dnd/focus top accents if retained. Keep `align-items: center` column layout, generous desktop padding (existing media query).

- [ ] **Step 3: Pinned manual check — file dialog still opens**

With HMR at `http://localhost:9000/register` (current layout, dropzone still mounted in old frame):
1. Click the CTA area → file dialog opens.
2. Click empty frame area → dialog opens.
3. Tab to zone, press Enter → dialog opens.
4. Drop a >10 MB PDF → toast `File exceeds the 10 MB limit.`; drop a .txt → `Only PDF files are accepted.`
Expected: all four pass. If clicks on the CTA no longer open the dialog, the slot content is above the native — fix stacking (do **not** remove the native overlay; add `pointer-events: none` to slot-only decorations and re-check).

- [ ] **Step 4: Verify compile + statics**

Run: `cd frontend && npm run typecheck && npm run lint:check`
Expected: both exit 0.

- [ ] **Step 5: Contrast audit (trust row + CTA)**

Pairs: white on `--color-primary` (documented 10.33:1 ✓), trust-row muted/secondary on `--color-surface` — confirm documented or compute.
Expected: no pair < 4.5:1; record new values.

- [ ] **Step 6: Commit**

```bash
git add frontend/src/components/Form5Dropzone.vue frontend/src/components/AttachmentUploader.vue
git commit -m "fix: dropzone full-width root cause + mockup restyle (dashed frame, CTA, trust row)"
```

---

### Task 7: register.vue rewire + step-frame changes

**Files:**
- Modify: `frontend/src/pages/register.vue` (template rewrite, styles, small script changes)
- Modify: `frontend/src/pages/register/components/UploadStep.vue` (remove AppCard)
- Modify: `frontend/src/pages/register/components/ReviewStep.vue` (remove own head)
- Modify: `frontend/src/pages/register/components/DoneStep.vue` (remove AppCard)

**Interfaces:**
- Consumes: `RegisterWorkspace`, `DocketPanel`, `StepOverviewCard`, `PrivacyCard`, `GuidelinesCard` (Tasks 1–5).
- Produces: the integrated register page. Flow contract change (pinned, spec §6.4): parse **no longer auto-advances**; an explicit Continue does.

- [ ] **Step 1: Strip superseded frames from step components**

- `UploadStep.vue`: delete the `AppCard` wrapper and its `#subtitle` (copy lives in the sidebar + dropzone now); template = `<Form5Dropzone …/><ParseLog …/>` (drop the AppCard import; comment updated). Props/emits unchanged.
- `DoneStep.vue`: delete the `AppCard` wrapper (read the file first; keep its inner receipt content and `restart` emit).
- `ReviewStep.vue`: delete the `review-slip__head` block (h2 `Step 2: Verify your details` + `AppChip`) — the DocketPanel header supersedes it; the chip moves to the panel `meta` slot (Step 3). Rest of the slip (panes, q-form, internal actions footer) unchanged; drop now-unused imports.

- [ ] **Step 2: Rewrite `register.vue` template**

```
<RegisterWorkspace :step="step" :max-reached="maxReached" :finished="finished"
                   @jump="onJump">
  <template #sidebar>
    <StepOverviewCard :eyebrow="overview.eyebrow" :title="overview.title">
      {{ overview.body }}
      <template #status>{{ per-step status box (below) }}</template>
    </StepOverviewCard>
    <PrivacyCard />
    <GuidelinesCard ref="guidelines" variant="…" />
  </template>
  <template #panel>
    <DocketPanel eyebrow="DOCKET FORM 5-A" :title="panelTitle">
      <template #meta>…per-step…</template>
      <UploadStep v-if="step === 0" …all current bindings… />
      <ReviewStep v-else-if="step === 1 && parsed" …all current bindings… />
      <DoneStep v-else-if="step === 2" …all current bindings… />
      <template #actions v-if="step === 0">…buttons (Step 4)…</template>
    </DocketPanel>
  </template>
</RegisterWorkspace>
<OcrConfidenceDialog …unchanged… />
```

Pinned per-step data (script computeds/copy):
- `panelTitle`: `["Upload Form 5 PDF", "Verify Student Data", "Issuance & Confirmation"][step]`
- `#meta`: step 0 → `MAX SIZE: {{ formatBytes(MAX_PDF_BYTES) }}`; step 1 → `<AppChip :label="mode === 'raster' ? 'OCR FALLBACK' : 'TEXT-LAYER PARSE'" …>` (moved from ReviewStep) + `{{ filledCount }}` where `filledCount = computed(() => \`${nonEmpty}/${total}\`)` over `Object.entries(draft)` with `total = Object.keys(draft).length` and nonEmpty counting trimmed non-empty strings; step 2 → `REF ID · {{ referenceId }}`
- Sidebar `overview`: step 0 → eyebrow `— STEP 01 / OVERVIEW`, title `Matriculation Verification`, body `Provide your official UP Form 5 (Electronic or Scanned PDF). Runs entirely inside your browser — your Form 5 never leaves this device.`; step 1 → `— STEP 02 / OVERVIEW` / `Verify Student Data` / `Review the roster fields extracted from your Form 5, attach your photo and signature, and confirm RA 10173 consent.`; step 2 → `— STEP 03 / OVERVIEW` / `Issuance & Confirmation` / `Your registration has been recorded. Keep the reference ID below as your proof of submission.`
- Status box (slot content): step 0 → label `PARSER ENGINE`, value `FORM5-PARSER · SIM v1.8.4`, pill `● READY` when `!isParsing` else `● PARSING` (dot `--color-primary`; **no ERROR state** — `useForm5Parse` has no failure path; documenting deviation from spec §6.2's ERROR, honest per D3); step 1 → `FIELDS EXTRACTED` + `filledCount`; step 2 → `REFERENCE ID` + `referenceId`.
- `GuidelinesCard` variant: `["upload", "review", "next"][step]`.

- [ ] **Step 3: Flow changes in `register.vue` script**

1. `enterReview`: remove `step.value = 1` (keep `maxReached` bump removal too) — parsed payload lands while still on step 0; `ocrDialogOpen` logic unchanged.
2. Add `function onContinue() { if (!parsed.value || isParsing.value) return; step.value = 1; maxReached.value = Math.max(maxReached.value, 1); }`.
3. Add `function onJump(i: number) { if (reached(i)) step.value = i; }` (PhaseStrip gates rendering; this is the belt).
4. Add `const guidelines = ref<InstanceType<typeof GuidelinesCard> | null>(null)` + `function focusGuidelines() { guidelines.value?.$el?.scrollIntoView({ behavior: "smooth", block: "nearest" }); (guidelines.value?.$el as HTMLElement | undefined)?.focus({ preventScroll: true }); }` (adapt to actual `$el` typing; card root gets `tabindex="-1"` fallthrough from register).
5. Header meta needs `formatBytes` (`@/domain/roster`) + `MAX_PDF_BYTES` (`@/domain/validation`) imports.

- [ ] **Step 4: Actions slot (step 0 only)**

- Primary: `q-btn` label `CONTINUE TO STEP 02`, `color="primary"`, `:disable="!parsed || isParsing"`, `@click="onContinue"`.
- Secondary: `q-btn` outline label `GUIDELINES & FAQ`, `@click="focusGuidelines"`.
- Steps 1/2: **no actions slot** (ReviewStep keeps its internal form footer; DoneStep keeps its own).

- [ ] **Step 5: Delete QStepper remnants**

Remove `<q-stepper>`/`<q-step>` markup and the entire deep-stepper style block (register.vue:219–301); keep `.register-shell { min-width: 0; }` (rename only if trivial). `$q` stays (used by `notify`).

- [ ] **Step 6: Pinned manual check — full wizard flow**

At `http://localhost:9000/register` (HMR):
1. Phase strip: 01 active (white cell, maroon rule), 02/03 muted with `PENDING PARSING` / `FINAL STAGE` eyebrows.
2. Sidebar shows overview + privacy + guidelines (`upload`); status pill reads `● READY`.
3. Dropzone spans the **full panel width** (original bug — half-width = FAIL).
4. Select a PDF → pill flips to `● PARSING`, ParseLog announces (aria-live), parse completes → **stays on step 0**, Continue enables → click → step 2 view (panel title `Verify Student Data`, sidebar variant `review`, meta shows chip + `n/6`).
5. Back-jump: click phase cell 01 → returns; guards hold.
6. Fill fields, attach photo/signature, consent, submit → step 3; strip shows 01/02 done, 03 active; clicking any cell does nothing (finished lock); sidebar variant `next`; meta shows `REF ID · REG-…`.
7. Start over → resets to step 0, strip unlocked.
Expected: all 7 pass. **On any failure: STOP (report, propose fix, get approval) — do not auto-fix.**

- [ ] **Step 7: Verify compile + statics**

Run: `cd frontend && npm run typecheck && npm run lint:check && npm run build`
Expected: all exit 0.

- [ ] **Step 8: Commit**

```bash
git add frontend/src/pages/register.vue \
        frontend/src/pages/register/components/UploadStep.vue \
        frontend/src/pages/register/components/ReviewStep.vue \
        frontend/src/pages/register/components/DoneStep.vue
git commit -m "feat(register): workspace layout replaces QStepper frame; explicit Continue"
```

---

### Task 8: Stationery footer (MainLayout)

**Files:**
- Modify: `frontend/src/layouts/MainLayout.vue` (footer markup + `.app-footer` styles only — lines ~147–151, ~304–311)

**Interfaces:**
- Consumes: none.
- Produces: new footer shown on register + admin (spec §6.6).

- [ ] **Step 1: Replace footer markup + styles**

Markup (replace current text node): left block = maroon square span (`--color-secondary`, `--spacing-3` box) + `University of the Philippines · Office of Student Affairs & Institutional Registrars`, second line `Frontend prototype, simulation only — no live registration.`; right block = three plain `<span>` labels `DATA PRIVACY MANUAL` · `SYSTEM TERMS` · `STATIONERY SPEC 03-A` — **not links, no `href`, no cursor:pointer** (spec §6.6: dead links are worse than labels).
Styles: `.app-footer` becomes `display: flex; flex-wrap: wrap; justify-content: space-between; align-items: baseline; gap; text-align: left` (replacing `text-align: center`); right labels mono uppercase `--tracking-eyebrow` muted; keep `border-top: 1px solid var(--color-border)` and caption sizing.
**Do not touch the `<q-header>` letterhead block** (D1).

- [ ] **Step 2: Verify compile + statics**

Run: `cd frontend && npm run typecheck && npm run lint:check`
Expected: both exit 0.

- [ ] **Step 3: Manual check — both pages, navbar intact**

1. `http://localhost:9000/register` and `/admin`: new footer renders, stacks below 640px, right labels are non-interactive.
2. Letterhead unchanged (visual compare against pre-task state; git diff of the file shows changes only inside footer markup/styles).
Expected: pass; diff contains no letterhead hunks.

- [ ] **Step 4: Commit**

```bash
git add frontend/src/layouts/MainLayout.vue
git commit -m "feat(layout): stationery footer with preserved simulation notice"
```

---

### Task 9: Docs side-task — limit corrections (spec §12/D4)

**Files:**
- Modify: `PRODUCT.md` (line 58)
- Modify: `PRD.md` (lines 40, 140)

**Interfaces:**
- Consumes: code constants (`MAX_PDF_BYTES` 10 MB, `MAX_IMAGE_BYTES` 5 MB) are authoritative (D4).

- [ ] **Step 1: Apply exact corrections**

- `PRODUCT.md:58` → `- **Limits:** PDF ≤ 10 MB; photo/signature JPG/PNG ≤ 5 MB each.`
- `PRD.md:40` → `Dropzone accepts PDF only, max 10 MB. Non-PDF → toast \`Only PDF files are accepted.\` Oversize → \`File exceeds the 10 MB limit.\` (interpolated from the enforced constant).` (exact toast string matches `formatBytes(10485760)` = `10 MB`, roster.ts:76-83)
- `PRD.md:140` → `- Upload limits: PDF 10 MB, images 5 MB each (~20 MB/member ceiling).`

- [ ] **Step 2: Verify no other stale limit mentions**

Run: `grep -rn "5 MB\|2 MB" PRODUCT.md PRD.md` — review every remaining hit; each must be a deliberately correct context (e.g. none should state the PDF ceiling as 5 MB or image ceiling as 2 MB).
Expected: no stale ceiling claims.

- [ ] **Step 3: Commit**

```bash
git add PRODUCT.md PRD.md
git commit -m "docs: align stated upload limits with enforced constants (10 MB / 5 MB)"
```

---

### Task 10: Final verification + user review gate

**Files:** none (verification only).

- [ ] **Step 1: Full static gate**

Run: `cd frontend && npm run typecheck && npm run lint:check && npm run build`
Expected: all exit 0. **On failure: STOP → report → propose fix → get approval.**

- [ ] **Step 2: Review Focus checklist (manual, `http://localhost:9000/register`)**

1. *Finished lock*: complete a registration → click every phase-strip cell → no jump (RF-1).
2. *Dropzone width*: zone spans full panel width at desktop and stacks full-width <900px (RF-2).
3. *Dialog opens*: click CTA / empty frame / Enter-on-focus all open the file dialog; both reject toasts fire (RF-3).
4. *a11y*: `aria-current="step"` on active cell; ParseLog announces new lines while parsing; `GUIDELINES & FAQ` scrolls + moves focus to the guidelines card (Tab order confirms); dropzone focus ring visible (RF-4).
5. *Contrast*: every new pair from Tasks 1/3/6/8 recorded ≥4.5:1 — none pending (RF-5).
6. Layout: <900px stack order bar → strip → panel → sidebar; footer stacks <640px; navbar byte-identical (git diff shows footer-only hunks in MainLayout).

- [ ] **Step 3: User screenshot review (spec §10.4)**

Show/ask the user to review the rendered register page against their mockup (they view `localhost:9000` and share screenshots, per session flow). Collect changes; **if any requested change fails a check, stop and report before fixing.**
Expected: user sign-off.

- [ ] **Step 4: Final commit (only if Step 3 produced fixes)**

```bash
git add -A && git commit -m "fix(register): review adjustments from screenshot sign-off"
```
