<script setup lang="ts">
import { computed } from "vue";

/** Status chip: positive (vector / dedup) and cautionary (OCR fallback). */
const props = withDefaults(
  defineProps<{ label: string; tone?: "positive" | "caution" | "neutral" }>(),
  { tone: "neutral" }
);

// Tone -> stamp cell. The Receipt Line reads state as stamped ink, so the
// mapping resolves to a cell class instead of a Quasar palette name; every
// ink-on-tint pair it lands on is measured in the style block below.
// Callers keep the same props and stay free of both vocabularies.
const STAMP: Readonly<Record<typeof props.tone, string>> = {
  positive: "app-chip--done",
  caution: "app-chip--caution",
  neutral: "app-chip--pending"
};

const stampClass = computed(() => STAMP[props.tone]);
</script>

<template>
  <!-- Rubber stamp: square-cut cell ruled once in its own ink, tracked small
       caps on the tint. The rule is the edge — no shadow rides with it. -->
  <q-chip square class="app-chip" :class="stampClass" :label="label" />
</template>

<style scoped lang="scss">
// Stamp cell — shared geometry: square, hairline rule, tracked small caps.
// The base carries the pending ink, so the default tone (and any tone a JS
// caller invents at runtime) still lands on a legible stamp instead of
// Quasar's grey. Pending: muted on sunken stock, 5.30:1.
//
// No .type-eyebrow here, deliberately. This is a <q-chip>, and app.scss's
// global .q-chip (caption / 700 / eyebrow tracking) lands AFTER .type-eyebrow
// at equal specificity (0-1-0), so a role class would lose. This scoped rule
// is 0-2-0 and already outranks the bridge — the register stays spelled out.
.app-chip {
  background: var(--color-surface-sunken);
  border: var(--border-hairline) solid var(--color-stamp-pending);
  border-radius: 0;
  box-shadow: var(--elevation-rest); // the rule is the only elevation
  color: var(--color-stamp-pending);
  font-size: var(--text-caption);
  font-weight: var(--weight-bold);
  letter-spacing: var(--tracking-eyebrow);
  line-height: var(--leading-caption);
  padding: var(--spacing-1) var(--spacing-3);
  text-transform: uppercase;
}

// Filed/done: maroon ink on its tint — 9.51:1, rule in the same ink.
.app-chip.app-chip--done {
  background: var(--color-stamp-bg);
  border-color: var(--color-stamp);
  color: var(--color-stamp);
}

// Caution: graphite ink on the amber wash (graphite on any *-soft surface
// measures 11.8–12.4:1). Solid amber outshouts the tint family, and an
// amber rule is 1.73:1 on paper — so the hue rides the wash and the edge
// stays ink.
.app-chip.app-chip--caution {
  background: var(--color-accent-soft);
  border-color: var(--color-foreground);
  color: var(--color-foreground);
}

// Focus: ink rule with the amber hairline hard against it (7.90:1); amber
// alone on paper is 1.73:1, so the ring never carries the state itself.
.app-chip:focus-visible {
  border-color: var(--color-foreground);
  outline: var(--border-rule) solid var(--color-rule-focus);
  outline-offset: 0;
}
</style>
