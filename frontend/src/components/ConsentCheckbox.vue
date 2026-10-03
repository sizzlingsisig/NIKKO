<script setup lang="ts">
defineProps<{ modelValue: boolean; invalid?: boolean }>();
const emit = defineEmits<{ "update:modelValue": [value: boolean] }>();
</script>

<template>
  <q-banner
    dense
    class="consent"
    :class="{
      'consent--stamped': modelValue,
      'consent--invalid': invalid
    }"
  >
    <template #avatar>
      <q-checkbox
        :model-value="modelValue"
        input-id="consent-box"
        size="24px"
        color="secondary"
        :aria-invalid="invalid"
        aria-describedby="consent-text"
        @update:model-value="emit('update:modelValue', $event === true)"
      />
    </template>

    <!-- `for` points at the QCheckbox input, so the whole sentence toggles it
         (q-banner renders a div, which cannot be a label host itself). -->
    <label id="consent-text" for="consent-box" class="consent__text type-body">
      I authorize <strong>UPV Student Organization</strong> to collect and
      process the operational metadata, photograph, and signature above strictly
      for member roster management in accordance with <strong>RA 10173</strong>.
    </label>
  </q-banner>

  <p v-if="invalid" class="consent__error type-body-strong" role="alert">
    RA 10173 consent is required.
  </p>
</template>

<style scoped lang="scss">
// Consent clause: a stamped frame on counterfoil stock — square-cut, hairline
// border, elevation declared once (the border; no shadow rides with it).
.consent {
  align-items: flex-start;
  background: var(--color-surface-sunken);
  border: var(--border-hairline) solid var(--color-rule-entry);
  border-radius: 0;
  box-shadow: none;
  color: inherit;
  display: flex;
  gap: var(--spacing-1);
  padding: var(--spacing-4);
}

// Claimed: ink frame with the amber hairline flush against it — the same
// pairing the slip frame uses (amber vs ink 7.90:1; amber never travels
// alone on paper).
.consent:focus-within {
  border-color: var(--color-foreground);
  outline: var(--border-rule) solid var(--color-rule-focus);
  outline-offset: 0;
}

// Granted: the clause takes the maroon stamp tint (ink on it 11.8–12.4:1)
// and the box takes maroon ink. Declared before the error state so an
// invalid frame always wins should both flags ever arrive together.
.consent--stamped {
  background: var(--color-stamp-bg);
  border-color: var(--color-stamp);
}

// Rejected: red-stamp frame — same tint the margin note below is stamped in.
.consent--invalid {
  background: var(--color-stamp-error-bg);
  border-color: var(--color-stamp-error);
}

// .type-body matches exactly (sans / body / 400 / --leading-body); this rule
// keeps the ink, the pointer and the measure.
.consent__text {
  color: var(--color-foreground);
  cursor: pointer;
  max-width: 68ch; // 60-80 character measure
}

// Unchecked: an empty ink-outlined stamp box on stock.
.consent :deep(.q-checkbox__inner) {
  color: var(--color-foreground);
}

// Checked: the maroon rubber stamp — white check on maroon 10.87:1. Same
// treatment as the done markers on the ticket strip.
.consent :deep(.q-checkbox__inner--truthy) {
  color: var(--color-stamp);
}

// The frame carries focus above; a second ring around the 24px box would
// double the indicator. The frame's ring shows for every focus, keyboard or
// not, so keyboard visibility is never lost here.
.consent :deep(.q-checkbox:focus-visible) {
  outline: none;
}

// Rejected: the sentence below is stamped into the margin — destructive ink
// on its tint (5.75:1 measured), square-cut frame, full 1px border, no
// colored side rail, no shadow.
//
// .type-body-strong matches exactly what this rule spelled out (body / 700 /
// --leading-body), so the swap is a no-op.
.consent__error {
  background: var(--color-stamp-error-bg);
  border: var(--border-hairline) solid var(--color-stamp-error);
  border-radius: 0;
  color: var(--color-stamp-error);
  margin: var(--spacing-2) 0 0;
  padding: var(--spacing-1) var(--spacing-3);
}

// Browser surfaces: selection takes the amber claim tint (graphite on it
// stays ≥4.5:1), so the clause selects inside the same world it prints in.
.consent__text::selection {
  background: var(--color-accent-soft);
  color: var(--color-foreground);
}
</style>
