<script setup lang="ts">
defineProps<{ modelValue: boolean }>();

const emit = defineEmits<{ "update:modelValue": [value: boolean] }>();
</script>

<template>
  <!-- Low OCR confidence gate (FR-1.3) -->
  <q-dialog
    :model-value="modelValue"
    @update:model-value="emit('update:modelValue', Boolean($event))"
  >
    <q-card class="ocr-dialog">
      <q-card-section class="ocr-dialog__head">
        <h3 class="ocr-dialog__title">⚠️ Low OCR confidence</h3>
      </q-card-section>
      <q-card-section class="ocr-dialog__body">
        Tesseract.js confidence is below the
        <span class="ocr-dialog__figure">75%</span> threshold for this scan. The
        extracted fields have been pre-filled. Please review and correct each
        highlighted field manually before submitting.
      </q-card-section>
      <q-card-actions align="right" class="ocr-dialog__actions">
        <q-btn
          unelevated
          color="primary"
          label="Review fields manually"
          @click="emit('update:modelValue', false)"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<style scoped lang="scss">
// Notice slip: square-cut counter-slip language from AppCard — white paper,
// hairline edge, elevation declared once (the 1px border, no shadow beside
// it). Beats the global .q-card rounded-card defaults back to square; the
// Quasar scrim behind it supplies the separation from the page.
.ocr-dialog {
  background: var(--color-surface);
  border: var(--border-hairline) solid var(--color-rule-hairline);
  border-radius: 0;
  box-shadow: none;
  // Slip measure up to 26rem, bounded by the viewport so the notice never
  // runs off a 320px screen.
  width: min(26rem, calc(100vw - 2 * var(--spacing-4)));
}

// Ruled head: the slip's own band treatment — maroon serif on paper
// (10.87:1), closed by a fine rule. The heading stands alone; no kicker line
// above it.
.ocr-dialog__head {
  border-bottom: var(--border-hairline) solid var(--color-rule-hairline);
  color: var(--color-secondary);
  padding: var(--spacing-4) var(--spacing-6);
}

.ocr-dialog__title {
  color: inherit;
  font-family: var(--font-serif);
  font-size: var(--text-subhead);
  font-weight: 700;
  line-height: var(--leading-tight);
  margin: 0;
}

// Paper body: muted ink on white (6.00:1), with the threshold figure
// stamped as a caution cell — the AppChip stamp voice (tracked small caps,
// square cut, hairline rule): graphite on the amber wash 12.40:1, edge
// carried by the ink hairline (the wash is 1.10:1 against paper, so it
// never rules itself). Mono because 75% is a measurement, not prose; the
// caption line box keeps the stamp inside the body's 24px leading.
.ocr-dialog__body {
  color: var(--color-foreground-muted);
  font-size: var(--text-body);
  line-height: var(--leading-body);
  padding: var(--spacing-4) var(--spacing-6);
}

.ocr-dialog__figure {
  background: var(--color-accent-soft);
  border: var(--border-hairline) solid var(--color-foreground);
  color: var(--color-foreground);
  display: inline-block;
  font-family: var(--font-mono);
  font-size: var(--text-caption);
  font-weight: 700;
  letter-spacing: var(--tracking-eyebrow);
  line-height: var(--leading-caption);
  padding: 0 var(--spacing-2);
  text-transform: uppercase;
}

// Ruled foot: the maroon rule closes the slip above the action strip
// (--border-rule is the sanctioned 2px for horizontal ruled lines).
.ocr-dialog__actions {
  border-top: var(--border-rule) solid var(--color-rule-strong);
  gap: var(--spacing-3);
  padding: var(--spacing-4) var(--spacing-6);
}

// Touch floor for the gate's only control. The global .q-btn min-height
// already reaches it; restated so the target survives a bridge change.
.ocr-dialog__actions .q-btn {
  min-height: var(--touch-target);
}

// Focus = amber hairline hard against the button's own teal edge (5.96:1 —
// amber floating on paper is 1.73:1, so the ring never carries the state
// alone). Radius hugs the button so the ring reads as ruled around it;
// outranks the global :focus-visible teal ring.
.ocr-dialog .q-btn:focus-visible {
  border-radius: var(--radius-md);
  outline: var(--border-rule) solid var(--color-rule-focus);
  outline-offset: 0;
}
</style>
