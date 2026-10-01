<script setup lang="ts">
// PhaseStrip: the register wizard's progress indicator — three ruled cells
// (mono badge, eyebrow, title) carrying the visual role QStepper's header
// used to play. State rides three props; a reachable phase renders its whole
// body as one real button emitting the jump, an unreached one as an
// aria-disabled span — guarded by the caller exactly as the stepper's
// header-nav was.

const props = defineProps<{
  step: number;
  maxReached: number;
  finished: boolean;
}>();

const emit = defineEmits<{ jump: [step: number] }>();

// Pinned copy: the three phases and their pending-state eyebrows.
const TITLES = [
  "UPLOAD YOUR FORM 5",
  "VERIFY STUDENT DATA",
  "ISSUANCE & CONFIRMATION"
];
const PENDING_EYEBROWS = ["", "PENDING PARSING", "FINAL STAGE"];

/** Zero-padded mono cell number ("01"). */
function badge(i: number): string {
  return String(i + 1).padStart(2, "0");
}

/** State label: "ACTIVE PHASE" on the current cell, "PHASE COMPLETE" on
 *  every cell before it, otherwise the pinned pending eyebrow. */
function eyebrow(i: number): string {
  if (i === props.step) return "ACTIVE PHASE";
  if (i < props.step) return "PHASE COMPLETE";
  // Index is always in range here (PENDING_EYEBROWS[0] is only ever read
  // for i > step, which i = 0 can never satisfy); the fallback keeps
  // noUncheckedIndexedAccess quiet without changing that behaviour.
  return PENDING_EYEBROWS[i] ?? "";
}

/** Filed: the cell sits before the current phase. */
function done(i: number): boolean {
  return i < props.step;
}

/** The cell the wizard is standing on. */
function active(i: number): boolean {
  return i === props.step;
}

/** Not yet reached (or locked out by the finished receipt). */
function pending(i: number): boolean {
  return i > props.step;
}

/** Reachable cells are real controls; the finished receipt locks them all. */
function reachable(i: number): boolean {
  return !props.finished && i <= props.maxReached;
}

/** Both body forms carry the handler; the guard keeps a click on the
 *  aria-disabled span (mouse only — it never takes focus) from emitting. */
function onJump(i: number): void {
  if (reachable(i)) emit("jump", i);
}
</script>

<template>
  <!-- Three ruled phase cells. The whole step is the control: when the phase
       is reachable its body (badge + eyebrow + title) renders as one real
       button emitting jump(i); otherwise it is an aria-disabled span. The
       active body carries aria-current="step". List markers are stripped
       (the mono badges do the numbering), so role="list" holds the semantics
       VoiceOver drops when a list renders without markers. -->
  <ol class="phase-strip" role="list">
    <li
      v-for="(title, i) in TITLES"
      :key="title"
      class="phase-strip__cell"
      :class="{
        'phase-strip__cell--active': active(i),
        'phase-strip__cell--done': done(i),
        'phase-strip__cell--pending': pending(i)
      }"
    >
      <component
        :is="reachable(i) ? 'button' : 'span'"
        class="phase-strip__body"
        :type="reachable(i) ? 'button' : undefined"
        :aria-disabled="reachable(i) ? undefined : 'true'"
        :aria-current="active(i) ? 'step' : undefined"
        @click="onJump(i)"
        ><span class="phase-strip__badge">{{ badge(i) }}</span
        ><span v-if="eyebrow(i)" class="phase-strip__eyebrow">{{
          eyebrow(i)
        }}</span
        ><span class="phase-strip__title">{{ title }}</span></component
      >
    </li>
  </ol>
</template>

<style scoped lang="scss">
// One row of equal cells, hairline-ruled like every other control boundary
// on the page (rule-entry, 3.48:1). Compact is the base — the <900px case —
// and the strip grows only at ≥900px, so a narrow screen never drops a cell
// or hides any of the three lines.
.phase-strip {
  display: grid;
  gap: var(--spacing-1);
  grid-template-columns: repeat(3, minmax(0, 1fr));
  list-style: none;
  margin: 0;
  padding: 0;
}

// The cell: the ruled block and its state ink. Its single child — the body
// below — stretches to fill it, so the whole step is one target.
.phase-strip__cell {
  border: var(--border-hairline) solid var(--color-rule-entry);
  display: grid;
  min-width: 0;
  padding: var(--spacing-2);
}

// Pending: no fill, muted ink — 6.00:1 on paper (documented), 5.59:1 on the
// canvas this page rests on; both clear AA 4.5:1.
.phase-strip__cell--pending {
  color: var(--color-foreground-muted);
}

// Active: the paper card with the heavy maroon rule at its foot — the same
// rule that closes the AppCard header. Ink on its white card 13.69:1.
.phase-strip__cell--active {
  background: var(--color-surface);
  border-bottom: var(--border-rule) solid var(--color-rule-strong);
  color: var(--color-foreground);
}

// Filed: the rubber-stamp pair the stepper's done cells wore — maroon ink on
// its tint, rule in the same ink (9.51:1, app.scss stamp tokens).
.phase-strip__cell--done {
  background: var(--color-stamp-bg);
  border-color: var(--color-stamp);
  color: var(--color-stamp);
}

// The step body: badge, eyebrow, title stacked — the cell's one control.
// Left-aligned because the reachable form is a button, whose UA default
// centres its children.
.phase-strip__body {
  display: grid;
  gap: var(--spacing-1);
  min-width: 0;
  text-align: left;
}

// The reachable body is a real <button>: strip the UA chrome and font so it
// reads as the cell itself, taking the cell's ink (pending muted, active
// ink, done stamp). Focus lands the global :focus-visible ring (10.33:1).
button.phase-strip__body {
  appearance: none;
  background: none;
  border: 0;
  color: inherit;
  cursor: pointer;
  font: inherit;
  margin: 0;
  padding: 0;
}

// Badge & eyebrow share the mono ticket voice: caption size, tracked like an
// eyebrow. Vertical padding only, so the number stays flush with the text
// beneath it — the target it contributes to is the whole body.
.phase-strip__badge,
.phase-strip__eyebrow {
  font-family: var(--font-mono);
  font-size: var(--text-caption);
  letter-spacing: var(--tracking-eyebrow);
  line-height: var(--leading-caption);
  padding: var(--spacing-1) 0;
  text-align: left;
}

// The title: the stepper's own header voice — caption-size bold caps — but
// untracked, since only badges and eyebrows carry the eyebrow tracking.
.phase-strip__title {
  font-size: var(--text-caption);
  font-weight: 700;
  line-height: var(--leading-caption);
  overflow-wrap: break-word; // narrowest phones may break a long word
}

@media (min-width: 900px) {
  .phase-strip {
    gap: var(--spacing-2);
  }

  .phase-strip__cell {
    padding: var(--spacing-3) var(--spacing-4);
  }
}
</style>
