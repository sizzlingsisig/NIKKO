<script setup lang="ts">
withDefaults(
  defineProps<{
    title?: string;
    subtitle?: string;
    /** Renders the slip step code (e.g. "Step 1") in the header band. */
    eyebrow?: string;
  }>(),
  { title: "", subtitle: "", eyebrow: "" }
);
</script>

<template>
  <q-card flat bordered class="app-card">
    <!-- Slip vocabulary: the filing code rides a quiet line above the maroon
         serif title, both on paper; subtitle and actions sit on the strip
         below, closed by the strong maroon rule. Each block renders when
         content arrives by prop *or* by slot, so a caller can pass rich
         markup (e.g. a <strong> in the subtitle) without the prop default
         of "" silently swallowing it. -->
    <header v-if="eyebrow || title" class="app-card__band">
      <p v-if="eyebrow" class="app-card__eyebrow type-eyebrow">{{ eyebrow }}</p>
      <h2 v-if="title" class="app-card__title">{{ title }}</h2>
    </header>

    <div
      v-if="subtitle || $slots.subtitle || $slots.actions"
      class="app-card__subhead"
    >
      <p v-if="subtitle || $slots.subtitle" class="app-card__subtitle"
        ><slot name="subtitle">{{ subtitle }}</slot></p
      >
      <div v-if="$slots.actions" class="app-card__actions"
        ><slot name="actions"
      /></div>
    </div>

    <q-card-section class="app-card__body">
      <slot />
    </q-card-section>
  </q-card>
</template>

<style scoped lang="scss">
// Slip frame: square-cut white paper. Elevation is declared once — as the
// shadow, not as the border — so no second frame rides alongside it. The
// hairline edge is gone from the resting card; --elevation-raised is the only
// lift it carries. radius/box-shadow beat the global .q-card rounded-card
// defaults (the global's shadow happens to match; ours is stated so the frame
// is this card's own decision, not an inherited one).
.app-card {
  background: var(--color-surface);
  border: none;
  border-radius: 0;
  box-shadow: var(--elevation-raised);
}

// Keyboard focus anywhere inside the slip: ink hairline with an amber hairline
// hard against it. Amber vs ink 7.90:1; amber alone on paper is 1.73:1 (never).
// The ink half used to be the card's own `border`, which paints INSIDE the
// border box. With the border gone that would be a no-op and the amber outline
// would sit straight on white at 1.73:1 — under the 3:1 WCAG 1.4.11 floor.
//
// The ink now rides as a shadow ring, which paints OUTSIDE the border box. That
// is not the pixel the border used to occupy, and `outline-offset: 0` would put
// the amber over the top of it — the ink would be invisible and the amber's
// inner edge would touch the card's own white surface. Offsetting the outline by
// one hairline starts the amber where the ink ends, so the two are adjacent and
// the 7.90:1 adjacency is real. Order matters: the outline paints after the
// element's own shadows, so it must not overlap them.
.app-card:focus-within {
  box-shadow:
    var(--elevation-raised),
    0 0 0 var(--border-hairline) var(--color-foreground);
  outline: var(--border-rule) solid var(--color-rule-focus);
  outline-offset: var(--border-hairline);
}

// Paper, not slab. The header speaks the same voice as the letterhead: the
// title is maroon serif ink on stock, a fine rule separates it from the
// subhead row, and the strong maroon rule under that row closes the block
// before the body opens. No filled band anywhere on the page — the navbar
// draws maroon as rules and ink, so the cards do too.
.app-card__band {
  border-bottom: var(--border-hairline) solid var(--color-rule-hairline);
  color: var(--color-foreground);
  padding: var(--spacing-4) var(--spacing-6);
}

// Tracked small caps code (Step 1, FR-4.1) — the record's own filing data,
// so it stays on the card as quiet muted ink rather than a headline. The
// maroon tick in front of it is the only signal colour in the header.
// .type-eyebrow carries the register (size/weight/leading/tracking/uppercase);
// this rule keeps the flex row, the gap, the margin and the ink.
.app-card__eyebrow {
  align-items: center;
  color: var(--color-foreground-muted);
  display: flex;
  gap: var(--spacing-2);
  margin: 0 0 var(--spacing-2);
}

// A 24px maroon hairline. A length, not a gap: the spacing scale would let a
// future rhythm change resize a decorative tick. One consumer, so a literal
// rather than a token — same call as RosterTable's calc().
.app-card__eyebrow::before {
  background: var(--color-secondary);
  content: "";
  flex: none;
  height: var(--border-hairline);
  width: 1.5rem;
}

// Maroon serif on paper, 10.87:1 — the same voice and colour as the NIKKO
// lockup in the header, so a card title and the product name read as one hand.
// No role class: .type-subhead is sans and rides --leading-subhead (40px),
// where this wants the serif lockup voice on --leading-tight (32px). The
// weight is tokenised rather than left raw.
.app-card__title {
  color: var(--color-secondary);
  font-family: var(--font-serif);
  font-size: var(--text-subhead);
  font-weight: var(--weight-bold);
  line-height: var(--leading-tight);
  margin: 0;
}

// Paper strip under the band; the strong maroon rule closes the whole
// header block before the body starts.
.app-card__subhead {
  align-items: flex-start;
  border-bottom: var(--border-rule) solid var(--color-rule-strong);
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-3);
  justify-content: space-between;
  padding: var(--spacing-4) var(--spacing-6);
}

.app-card__subtitle {
  color: var(--color-foreground-muted);
  flex: 1 1 18rem;
  font-size: var(--text-body);
  line-height: var(--leading-body);
  margin: 0;
  max-width: 68ch; // 60-80 character measure
}

.app-card__actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-2);
}

.app-card__body {
  padding: var(--spacing-6);
}

// Header blocks carry their own padding, so the body sits tighter beneath
// them — and a body-only card keeps its full padding (q-card-section adds
// none of its own).
.app-card__band + .app-card__body,
.app-card__subhead + .app-card__body {
  padding-top: var(--spacing-4);
}

@media (min-width: 768px) {
  .app-card__band {
    padding: var(--spacing-6) var(--spacing-8);
  }

  .app-card__subhead {
    padding: var(--spacing-4) var(--spacing-8);
  }

  .app-card__body {
    padding: var(--spacing-8);
  }

  .app-card__band + .app-card__body,
  .app-card__subhead + .app-card__body {
    padding-top: var(--spacing-6);
  }
}
</style>
