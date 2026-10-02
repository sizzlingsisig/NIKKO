<script setup lang="ts">
import { onMounted, ref } from "vue";
import { isPdf, MAX_PDF_BYTES } from "@/domain/validation";
import { formatBytes } from "@/domain/roster";

const emit = defineEmits<{
  accept: [file: File];
  reject: [message: string];
}>();

/** Boundary validation: PDF only, 10 MB ceiling (FR-1). */
function offer(file: File | undefined) {
  if (!file) return;
  if (!isPdf(file.name, file.type)) {
    emit("reject", "Only PDF files are accepted.");
    return;
  }
  if (file.size > MAX_PDF_BYTES) {
    // Interpolated from the constant so the stated ceiling can never drift
    // away from the enforced one.
    emit("reject", `File exceeds the ${formatBytes(MAX_PDF_BYTES)} limit.`);
    return;
  }
  emit("accept", file);
}

/**
 * QFile's own `accept` filter drops non-matching files silently, which would
 * swallow the "Only PDF files are accepted." message. We let every file
 * through and validate it ourselves so the student always gets told why.
 *
 * The payload is a plain `File[]`; Quasar does not declare `onAdd` on
 * `QFileProps`, so the annotation here is the contract we rely on.
 */
function onAdd(files: readonly File[]) {
  offer(files[0]);
}

/**
 * Name the control where focus actually lands.
 *
 * QFile spreads fallthrough attrs onto the hidden `<input type="file">`
 * (`QFile.js:114`), which is `tabindex: -1` (`:108`) and `opacity: 0` — it can
 * never receive focus. The node that *does* take focus is `.q-field__native`,
 * a `<div tabindex="0">` built at `QFile.js:289-301` with no `role` and no name.
 * So an `aria-label` on `<q-file>` names an element no assistive tech ever
 * reports; the name has to go on the native node itself. Reading Quasar's
 * internals is the only way to reach it, hence this one direct DOM touch.
 */
const LABEL_ID = "form5-dropzone-label";

const root = ref<{ $el?: HTMLElement } | null>(null);

function nameFocusTarget(): void {
  const native = root.value?.$el?.querySelector(".q-field__native");
  if (!(native instanceof HTMLElement)) return;
  native.setAttribute("role", "button");
  native.setAttribute("aria-labelledby", LABEL_ID);
}

onMounted(nameFocusTarget);
</script>

<template>
  <q-file
    ref="root"
    dropzone
    borderless
    class="dropzone"
    :model-value="null"
    @add="onAdd"
  >
    <!-- Document window of the slip: square-cut paper in a dashed hairline
         frame, the prompt copy set on ruled lines, the visual CTA and the
         stationery trust row. The slot draws this box rather than restyling
         Quasar's `.q-file__dropzone`, so the look does not depend on which
         element QFile wraps it in. -->
    <div class="dropzone__inner">
      <span class="dropzone__icon" aria-hidden="true">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 120 150"
          width="120"
          height="150"
          fill="none"
        >
          <!-- Subtle document drop shadow -->
          <defs>
            <filter
              id="doc-shadow"
              x="-10%"
              y="-10%"
              width="125%"
              height="125%"
              filterUnits="userSpaceOnUse"
            >
              <feDropShadow
                dx="0"
                dy="2"
                stdDeviation="3"
                flood-color="#1b1c1d"
                flood-opacity="0.08"
              />
            </filter>
          </defs>

          <!-- Document Paper Body with Dog-ear Corner -->
          <path
            d="M 15 10 L 80 10 L 105 35 L 105 140 L 15 140 Z"
            fill="#FFFFFF"
            stroke="#791C24"
            stroke-width="2"
            stroke-linejoin="round"
            filter="url(#doc-shadow)"
          />

          <!-- Folded Dog-ear Corner -->
          <path
            d="M 80 10 L 80 35 L 105 35 Z"
            fill="#F8F3EF"
            stroke="#791C24"
            stroke-width="1.5"
            stroke-linejoin="round"
          />

          <!-- UP / F-5 Institutional Form Header Stamp -->
          <text
            x="32"
            y="32"
            font-family="'Plus Jakarta Sans', Arial, sans-serif"
            font-size="11"
            font-weight="700"
            fill="#791C24"
            letter-spacing="0.05em"
          >
            UP
          </text>
          <line
            x1="58"
            y1="20"
            x2="58"
            y2="34"
            stroke="#D1CDC7"
            stroke-width="1"
          />
          <text
            x="66"
            y="32"
            font-family="'JetBrains Mono', monospace"
            font-size="9"
            font-weight="600"
            fill="#6B6661"
          >
            F-5
          </text>

          <!-- Subtle Ruled Document Content Lines -->
          <line
            x1="30"
            y1="46"
            x2="90"
            y2="46"
            stroke="#E6E0DA"
            stroke-width="2"
            stroke-linecap="round"
          />
          <line
            x1="30"
            y1="56"
            x2="90"
            y2="56"
            stroke="#E6E0DA"
            stroke-width="2"
            stroke-linecap="round"
          />
          <line
            x1="30"
            y1="66"
            x2="75"
            y2="66"
            stroke="#E6E0DA"
            stroke-width="2"
            stroke-linecap="round"
          />

          <!-- Official Wine Maroon 2px Divider Rule -->
          <line
            x1="30"
            y1="78"
            x2="90"
            y2="78"
            stroke="#791C24"
            stroke-width="1.5"
          />

          <!-- Secondary Form Spec Lines -->
          <line
            x1="30"
            y1="88"
            x2="85"
            y2="88"
            stroke="#EFEAE4"
            stroke-width="1.5"
            stroke-linecap="round"
          />
          <line
            x1="30"
            y1="96"
            x2="65"
            y2="96"
            stroke="#EFEAE4"
            stroke-width="1.5"
            stroke-linecap="round"
          />

          <!-- PDF Badge / Plate at bottom -->
          <rect x="36" y="112" width="48" height="18" fill="#791C24" rx="2" />
          <text
            x="60"
            y="125"
            font-family="'JetBrains Mono', 'Plus Jakarta Sans', monospace"
            font-size="10"
            font-weight="700"
            fill="#FFFFFF"
            text-anchor="middle"
            letter-spacing="0.08em"
          >
            PDF
          </text>
        </svg>
      </span>

      <div class="dropzone__prompt">
        <!-- Referenced by aria-labelledby in nameFocusTarget(): the prompt
             doubles as the control's accessible name, so it is never "a file
             input" and never unnamed. -->
        <p :id="LABEL_ID" class="dropzone__lead">
          Drag and drop your official Form 5 PDF here
        </p>
        <p class="dropzone__alt">or browse from your computer</p>
      </div>

      <!-- Decorative only: the whole zone is the control and Quasar's native
           overlay owns the click, so this never takes pointer or focus
           events (aria-hidden says so out loud). -->
      <span class="dropzone__cta" aria-hidden="true">
        <span class="dropzone__cta-glyph">+</span> SELECT FORM 5 PDF
      </span>

      <!-- Stationery posture labels, not capability claims: where the parse
           runs and what the paper must carry. -->
      <div class="dropzone__trust">
        <p class="dropzone__trust-line">
          <span class="dropzone__trust-dot" aria-hidden="true">●</span>
          ON-DEVICE PROCESSING
        </p>
        <p class="dropzone__trust-line dropzone__trust-line--stamp">
          CRS / SAIS STAMP REQUIRED
        </p>
      </div>
    </div>
  </q-file>
</template>

<style scoped lang="scss">
.dropzone {
  width: 100%;

  // QField's own bottom rule would double up with the frame below.
  :deep(.q-field__control) {
    min-height: 0;
    padding: 0;
  }
}

// The window itself: square-cut paper in a dashed hairline frame (rule-entry
// is the 3.48:1 control boundary — the decorative hairline never guards a
// control; the panel supplies the maroon rule, so the solid head rule that
// used to close the slip block is gone from here).
//
// WHY width:100% — the half-width bug. Quasar lays
// `.q-field__control-container` out as a `row no-wrap` flex row; with the
// native overlay pulled out of flow (app.scss), this box is its only in-flow
// child and shrink-wraps to content on the main axis — flex stretch only
// applies to the cross axis. The q-file root already runs width:100%
// (`.dropzone`); the inner box was the missing piece.
.dropzone__inner {
  align-items: center;
  background: var(--color-surface);
  border: var(--border-hairline) dashed var(--color-rule-entry);
  border-radius: 0;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-4);
  // A drop target earns real estate: 32px of head/foot makes the window a
  // plausible tap surface rather than a letterbox around three short lines.
  padding: var(--spacing-8) var(--spacing-6);
  text-align: center;
  transition:
    background var(--duration-base) var(--ease-out),
    border-color var(--duration-base) var(--ease-out);
  width: 100%;
}

// Emblem: the Form 5 slip illustration — its dog-eared paper edge is the
// frame now, so the hairline stamp cell that used to wrap a 24px glyph is
// gone (at 48px none of the art's detail — F-5 stamp, rules, PDF badge —
// could read). Colors ship inside the art (#791C24 in the slip world's
// maroon register).
.dropzone__icon {
  align-items: center;
  display: flex;
  flex: none;
  justify-content: center;
}

.dropzone__icon svg {
  display: block;
  // 120px tall = 96px wide (120:150 art): the header stamp and badge stay
  // legible as texture without out-shouting the prompt line beneath.
  height: 120px;
  width: auto;
}

// Ruled prompt lines: the copy sits between two hairlines like an entry line
// waiting to be filled.
//
// `fit-content` is the fix for the hollow centre: a fixed 30rem capped these
// rules at 480px around ~200px of copy, so the hairlines ran far past the words
// and the middle of the window read as empty scaffolding. Shrink-wrapping makes
// the rules an entry line that hugs its text; `max-width` keeps them from
// overflowing once the copy wraps on a narrow screen.
.dropzone__prompt {
  border-bottom: var(--border-hairline) solid var(--color-rule-hairline);
  border-top: var(--border-hairline) solid var(--color-rule-hairline);
  max-width: 100%;
  padding: var(--spacing-3) 0;
  width: fit-content;
}

// The one instruction the student has to act on, so it carries subhead weight
// and outranks the `AppCard` title that contains it (also subhead, but serif
// and maroon — a different voice at the same size, not a louder one).
.dropzone__lead {
  color: var(--color-foreground);
  font-size: var(--text-subhead);
  font-weight: 700;
  line-height: var(--leading-subhead);
  margin: 0;
}

// The fallback path, deliberately a full step down and set as a link
// affordance: underlined maroon like the uploader's stamped action, because
// this is the line that actually invites the click-to-browse.
.dropzone__alt {
  color: var(--color-secondary); // maroon on white 10.87:1
  font-size: var(--text-caption);
  line-height: var(--leading-caption);
  margin: var(--spacing-1) 0 0;
  text-decoration: underline;
  text-decoration-color: var(--color-rule-strong);
  text-decoration-thickness: var(--border-hairline);
  text-underline-offset: var(--spacing-1);
}

// The visual CTA: a stamped instruction, not a control — the whole zone is
// the control and the overlaid native owns the click (the template marks it
// aria-hidden for exactly that reason). Mono, tracked, cut square like every
// other stamped label in the slip.
.dropzone__cta {
  background: var(--color-primary);
  color: var(--color-on-primary); // white on pine-teal 10.33:1
  font-family: var(--font-mono);
  font-size: var(--text-caption);
  font-weight: 700;
  letter-spacing: var(--tracking-eyebrow);
  line-height: var(--leading-caption);
  padding: var(--spacing-2) var(--spacing-4);
  text-transform: uppercase;
}

// The tracked mono set gives the "+" a gap it does not want; the glyph runs
// untracked so it reads as one mark against the words.
.dropzone__cta-glyph {
  letter-spacing: 0;
}

// Trust row: mono caption, centred (inherits the window's text-align), two
// lines of stationery posture — the parse runs here, the paper carries those
// stamps.
.dropzone__trust {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-1);
}

.dropzone__trust-line {
  color: var(--color-foreground-muted); // 6.00:1 on white
  font-family: var(--font-mono);
  font-size: var(--text-caption);
  line-height: var(--leading-caption);
  margin: 0;
}

// The dot is the status mark: pine-teal where the words are muted.
.dropzone__trust-dot {
  color: var(--color-primary); // 10.33:1 on white
}

// The stamp line inks maroon — it is the requirement, not the posture.
.dropzone__trust-line--stamp {
  color: var(--color-secondary); // 10.87:1 on white
}

// Hover: paper warms to sunken stock; the boundary stays the control rule.
.dropzone:hover .dropzone__inner {
  background: var(--color-surface-sunken);
}

// Focus (AppCard's claim frame): ink hairline with the amber hairline hard
// against it — amber vs ink 7.90:1, amber alone on paper is 1.73:1 (never).
// The outline rides the component root because `.q-field__control` clips its
// children (overflow: hidden), so an outline on the inner box never shows.
.dropzone:focus-within {
  outline: var(--border-rule) solid var(--color-rule-focus);
  outline-offset: 0;
}

.dropzone:focus-within .dropzone__inner {
  border-color: var(--color-foreground);
  border-style: solid;
  // The claim keeps its maroon top accent through every state.
  border-top-color: var(--color-rule-strong);
}

// QFile marks the root `.q-file--dnd` while a file is over it: the window is
// claimed — amber paper lit inside the ink frame, same claim frame as focus.
.dropzone.q-file--dnd {
  outline: var(--border-rule) solid var(--color-rule-focus);
  outline-offset: 0;
}

.dropzone.q-file--dnd .dropzone__inner {
  background: var(--color-accent-soft); // graphite on tint 12.4:1
  border-color: var(--color-foreground);
  border-style: solid;
  border-top-color: var(--color-rule-strong);
}

@media (min-width: 768px) {
  // Desktop earns more air than the base now that the base is already
  // 32/24px — the window is the page's primary control, not a sidecar.
  .dropzone__inner {
    padding: var(--spacing-12) var(--spacing-8);
  }
}
</style>
