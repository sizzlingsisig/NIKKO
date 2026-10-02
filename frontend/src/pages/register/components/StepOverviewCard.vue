<script setup lang="ts">
// StepOverviewCard: the sidebar's per-step briefing card — filing eyebrow,
// serif headline, body copy, and a bordered status box carrying the step's
// machine readout (field tally, reference ID). Two props hold
// the pinned per-step copy and two slots hold the body and the status rows,
// so Task 7 swaps all four per step without the card knowing any wizard
// state. Single-root <article>: the caller's id/tabindex fallthrough lands
// on the card itself (the focus-target pattern Task 7 wires).

defineProps<{
  /** Filing line, passed whole ("— STEP 01 / OVERVIEW"). */
  eyebrow: string;
  /** Serif headline ("Matriculation Verification"). */
  title: string;
}>();
</script>

<template>
  <!-- Paper card: hairline edge, square corners, no shadow — elevation is
       the border alone (the AppCard idiom). Head block stacks eyebrow over
       headline; the body slot follows; when the caller passes #status, a
       hairline rule divides it from the bordered status box, whose mono
       caption grid renders flat children as label/value rows. -->
  <article class="step-overview-card">
    <div class="step-overview-card__head">
      <p class="step-overview-card__eyebrow">{{ eyebrow }}</p>
      <h3 class="step-overview-card__title">{{ title }}</h3>
    </div>

    <div class="step-overview-card__body"><slot /></div>

    <template v-if="$slots.status">
      <hr class="step-overview-card__rule" />
      <div class="step-overview-card__status"><slot name="status" /></div>
    </template>
  </article>
</template>

<style scoped lang="scss">
// Frame: white paper on the canvas, hairline edge, square corners, no
// shadow — the AppCard/DocketPanel idiom (elevation declared once, as the
// border). Blocks stack on a 12px rhythm; the head block below tightens
// the eyebrow-to-headline pair to 8px so they read as one unit.
.step-overview-card {
  background: var(--color-surface);
  border: var(--border-hairline) solid var(--color-rule-hairline);
  border-radius: 0;
  box-shadow: none;
  display: grid;
  gap: var(--spacing-3);
  padding: var(--spacing-6);
}

.step-overview-card__head {
  display: grid;
  gap: var(--spacing-2);
}

// Filing eyebrow — the caller passes the whole string, em dash included.
// Mono caption, tracked like every eyebrow on the page, muted ink
// (6.00:1 on this card's paper, documented app.scss). The uppercase
// transform keeps a caller's sentence-case line in the same voice; the
// pinned copy ships caps already, so it renders byte-identical
// (DocketPanel/AppCard's eyebrow pattern).
.step-overview-card__eyebrow {
  color: var(--color-foreground-muted);
  font-family: var(--font-mono);
  font-size: var(--text-caption);
  letter-spacing: var(--tracking-eyebrow);
  line-height: var(--leading-caption);
  margin: 0;
  text-transform: uppercase;
}

// Serif headline at the subhead scale the brief pins: maroon serif on
// paper (10.87:1) — the same ink as the AppCard and DocketPanel titles.
// Margin zeroed because it is an <h3>; break-word only rescues a caller
// token wider than the card. 700 is the only self-hosted Caslon weight.
.step-overview-card__title {
  color: var(--color-secondary);
  font-family: var(--font-serif);
  font-size: var(--text-subhead);
  font-weight: 700;
  line-height: var(--leading-tight);
  margin: 0;
  overflow-wrap: break-word;
}

// Body slot: body size, ink (13.69:1 on paper). Task 7 passes a bare
// string here, so the div's own margins are all that matter.
.step-overview-card__body {
  color: var(--color-foreground);
  font-size: var(--text-body);
  line-height: var(--leading-body);
}

// The hairline between body and status block — control-boundary ink
// (rule-entry, 3.48:1), the divider the workspace bars use. The border
// reset plus height:0 kill the UA's inset default, so only the token
// hairline renders.
.step-overview-card__rule {
  border: 0;
  border-top: var(--border-hairline) solid var(--color-rule-entry);
  height: 0;
  margin: 0;
  width: 100%;
}

// Status box: hairline-bordered readout in the machine voice. The box sets
// mono caption type and stacks its children as rows, so the caller's flat
// label/value/pill markup renders as the "mono caption label + value rows"
// the brief pins; the caller inks its own rows.
.step-overview-card__status {
  border: var(--border-hairline) solid var(--color-rule-entry);
  color: var(--color-foreground);
  display: grid;
  font-family: var(--font-mono);
  font-size: var(--text-caption);
  gap: var(--spacing-1);
  line-height: var(--leading-caption);
  padding: var(--spacing-3);
}

// ≥768px: padding grows the way AppCard's body and DocketPanel's blocks
// do (DESIGN.md — 24px mobile, 32px at 768px+).
@media (min-width: 768px) {
  .step-overview-card {
    padding: var(--spacing-8);
  }
}
</style>
