<script setup lang="ts">
// DocketPanel: the register workspace's document card — the ruled frame the
// step components (UploadStep, ReviewStep, DoneStep) render inside. It caps
// itself with the 2px maroon rule (the AppCard idiom, spec §6.4), carries the
// pinned eyebrow over the serif display title with the per-step meta floated
// right, and closes with an actions footer only when a step ships controls
// (steps without actions render no footer strip).
withDefaults(
  defineProps<{
    eyebrow?: string;
    title: string;
  }>(),
  { eyebrow: "DOCKET FORM 5-A" }
);
</script>

<template>
  <!-- Paper frame: maroon cap rule on top, hairline edges elsewhere, square
       corners. Header (eyebrow → serif title, meta slot pinned right) →
       body (default slot at AppCard's body rhythm) → footer, which ships
       only when the actions slot arrives — a step with no controls gets
       no footer strip. -->
  <article class="docket-panel">
    <header class="docket-panel__head">
      <div class="docket-panel__heading">
        <p class="docket-panel__eyebrow">{{ eyebrow }}</p>
        <h2 class="docket-panel__title">{{ title }}</h2>
      </div>
      <div v-if="$slots.meta" class="docket-panel__meta">
        <slot name="meta" />
      </div>
    </header>

    <div class="docket-panel__body">
      <slot />
    </div>

    <footer v-if="$slots.actions" class="docket-panel__foot">
      <div class="docket-panel__actions">
        <slot name="actions" />
      </div>
    </footer>
  </article>
</template>

<style scoped lang="scss">
// The frame: white paper, hairline edge, and the 2px maroon rule capping it
// (rule-strong = maroon, 10.87:1 on paper). Square corners, no shadow —
// elevation is the border alone, the AppCard idiom. Border is declared
// before border-top so the accent wins the cascade. Flex column so the
// panel can stretch to its workspace row (RegisterWorkspace fills it) with
// the header on the top edge and the footer on the bottom edge — the body
// below absorbs the slack.
.docket-panel {
  background: var(--color-surface);
  border: var(--border-hairline) solid var(--color-rule-hairline);
  border-radius: 0;
  border-top: var(--border-rule) solid var(--color-rule-strong);
  box-shadow: none;
  display: flex;
  flex-direction: column;
}

// Header: eyebrow over the title as one block on the left, meta slot
// floated right (margin-left: auto). flex-wrap lets the meta drop onto its
// own right-aligned line beneath the title when a long display title leaves
// it no room — see the heading note below for why the title never crushes
// instead. Padding mirrors AppCard's band so header, body and footer share
// one horizontal grid (6 base, 8 at ≥768px).
.docket-panel__head {
  align-items: flex-start;
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-3) var(--spacing-4);
  padding: var(--spacing-4) var(--spacing-6);
}

// The filing block: mono eyebrow stacked over the serif title. Deliberately
// no min-width override — the group's automatic minimum (the title's
// longest word) is what stops a long title from being squeezed by the meta
// slot when the row is tight; the meta wraps below the title instead.
.docket-panel__heading {
  display: grid;
  gap: var(--spacing-2);
}

// Pinned filing code: mono caption, tracked like every eyebrow on the page,
// muted ink — 6.00:1 on the panel's paper (documented, app.scss). The copy
// ships caps; the transform keeps a caller's sentence-case eyebrow in the
// same voice (AppCard's pattern).
.docket-panel__eyebrow {
  color: var(--color-foreground-muted);
  font-family: var(--font-mono);
  font-size: var(--text-caption);
  letter-spacing: var(--tracking-eyebrow);
  line-height: var(--leading-caption);
  margin: 0;
  text-transform: uppercase;
}

// The serif display title — the panel's voice: maroon serif on paper
// (10.87:1, the same ink as the cap rule and AppCard's serif titles) at the
// page's title scale. Zeroed margin because it is an <h2>; break-word only
// rescues a caller-supplied token longer than the panel itself.
.docket-panel__title {
  color: var(--color-secondary);
  font-family: var(--font-serif);
  font-size: var(--text-title);
  font-weight: 700;
  line-height: var(--leading-title);
  margin: 0;
  overflow-wrap: break-word;
}

// Per-step meta (max size, field count, reference ID): mono caption floated
// right of the heading. The auto margin pins it to the right edge of the
// row *and* right-aligns it on its own line when it wraps; muted so bare
// text nodes read as meta (6.00:1 on paper) while chips inside keep their
// own ink.
.docket-panel__meta {
  color: var(--color-foreground-muted);
  font-family: var(--font-mono);
  font-size: var(--text-caption);
  letter-spacing: var(--tracking-eyebrow);
  line-height: var(--leading-caption);
  margin-left: auto;
  text-align: right;
}

// Body: the default slot at AppCard's body rhythm — spacing-6 base,
// spacing-8 at ≥768px (declared below with the header/footer). flex: 1
// absorbs the extra height when the grid stretches the panel to match the
// sidebar column, so the footer stays pinned to the panel's bottom edge.
.docket-panel__body {
  flex: 1 0 auto;
  padding: var(--spacing-6);
}

// Footer: rendered only when the actions slot arrives, closed by a
// hairline — the control boundary (rule-entry, 3.48:1) because the actions
// live here. Right-aligned, wrapping row of buttons.
.docket-panel__foot {
  align-items: center;
  border-top: var(--border-hairline) solid var(--color-rule-entry);
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-3) var(--spacing-4);
  padding: var(--spacing-4) var(--spacing-6);
}

// Actions slot: right-aligned, wrapping row of buttons — the auto margin
// pins it to the right edge of the footer row.
.docket-panel__actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-2);
  justify-content: flex-end;
  margin-left: auto;
}

// ≥768px: header and footer breathe the way AppCard's band and subhead do,
// all on the body's 8 grid so every horizontal edge stays aligned.
@media (min-width: 768px) {
  .docket-panel__head {
    padding: var(--spacing-6) var(--spacing-8);
  }

  .docket-panel__body {
    padding: var(--spacing-8);
  }

  .docket-panel__foot {
    padding: var(--spacing-4) var(--spacing-8);
  }
}
</style>
