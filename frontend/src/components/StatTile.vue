<script setup lang="ts">
defineProps<{ value: number | string; label: string }>();
</script>

<template>
  <!-- Ledger tile: a ruled column head over one entry line. Deliberately NOT
       the hero-metric template (big number + accent + supporting stats) — a
       plain ruled tile is what the ledger page needs here. -->
  <q-card flat bordered class="stat-tile">
    <q-card-section class="stat-tile__cell">
      <p class="stat-tile__label type-eyebrow">{{ label }}</p>
      <p class="stat-tile__value">{{ value }}</p>
    </q-card-section>
  </q-card>
</template>

<style scoped lang="scss">
// Square-cut sunken stock; elevation declared once (the hairline border),
// so no shadow rides alongside it.
.stat-tile {
  background: var(--color-surface-sunken);
  border: var(--border-hairline) solid var(--color-rule-hairline);
  border-radius: 0;
  box-shadow: none;
}

.stat-tile__cell {
  padding: var(--spacing-4);
}

// Tracked small caps column head, closed by a ruled line — the head of a
// ledger column, not an eyebrow above a heading (no heading here at all).
// .type-eyebrow carries the register; this rule keeps the rule, ink and space.
.stat-tile__label {
  border-bottom: var(--border-hairline) solid var(--color-rule-hairline);
  color: var(--color-foreground-muted); // on sunken stock 5.30:1
  margin: 0 0 var(--spacing-2);
  padding-bottom: var(--spacing-2);
}

// Counts are real data — mono is sanctioned (never a costume), with
// tabular figures so columns of numbers align down the page. No role class:
// .type-data is mono at caption, and this count is a subhead statement.
.stat-tile__value {
  color: var(--color-foreground); // graphite on stock, AAA
  font-family: var(--font-mono);
  font-size: var(--text-subhead);
  font-variant-numeric: tabular-nums;
  font-weight: var(--weight-bold);
  line-height: var(--leading-tight);
  margin: 0;
  overflow-wrap: anywhere;
}
</style>
