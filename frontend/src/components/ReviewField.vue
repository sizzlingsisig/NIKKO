<script setup lang="ts">
import { computed, ref, watch } from "vue";

import { FIELD_LABELS, isFieldValid, RULES } from "@/domain/validation";
import type { FieldKey } from "@/domain/validation";

const props = withDefaults(
  defineProps<{
    field: FieldKey;
    modelValue: string;
    /** Options render a QSelect; omit for a free-text QInput. */
    options?: readonly string[] | undefined;
    /** Lets the student type a value that is not in `options` (degree program). */
    creatable?: boolean;
    placeholder?: string;
    sourceNote?: string;
    /** Parent raises this on a submit attempt so every error surfaces at once. */
    reveal?: boolean;
  }>(),
  {
    options: undefined,
    creatable: false,
    placeholder: "",
    sourceNote: "",
    reveal: false
  }
);

const emit = defineEmits<{ "update:modelValue": [value: string] }>();

const touched = ref(false);

const isValid = computed(() => isFieldValid(props.field, props.modelValue));
const showError = computed(
  () => (touched.value || props.reveal) && !isValid.value
);
const isSelect = computed(() => Boolean(props.options));
/** A value must sit on the line before it can be filed as done — an empty
 *  entry never reads as complete, whatever a future rule might accept. */
const hasValue = computed(() => props.modelValue.trim() !== "");
const showDone = computed(() => hasValue.value && isValid.value);

/** QSelect needs a non-empty sentinel to mean "nothing chosen yet". */
const SELECT_PLACEHOLDER = "Not stated";

const selectOptions = computed<readonly string[]>(() => [
  SELECT_PLACEHOLDER,
  ...(props.options ?? [])
]);

/**
 * QSelect emits `string | number | null` — the `number` is part of its public
 * contract even though every option here is a string, so the value is coerced
 * rather than narrowed away. `null` (or the placeholder) means "nothing chosen".
 */
function onUpdate(value: string | number | null) {
  const text = value === null ? "" : String(value);
  emit("update:modelValue", text === SELECT_PLACEHOLDER ? "" : text);
}

function onBlur() {
  touched.value = true;
}

// A value replaced by the parse pass re-evaluates immediately; a value the
// student cleared shows its error straight away.
watch(
  () => props.modelValue,
  (next, previous) => {
    if (previous !== undefined && next !== previous) touched.value = true;
  }
);
</script>

<template>
  <div class="review-field" :class="{ 'review-field--error': showError }">
    <q-select
      v-if="isSelect"
      :model-value="modelValue"
      :options="selectOptions"
      :label="FIELD_LABELS[field]"
      :error="showError"
      :error-message="RULES[field].message"
      :use-input="creatable"
      :new-value-mode="creatable ? 'add-unique' : undefined"
      input-debounce="0"
      outlined
      dense
      options-dense
      hide-bottom-space
      autocomplete="off"
      class="review-field__control"
      @update:model-value="onUpdate"
      @blur="onBlur"
    />

    <q-input
      v-else
      :model-value="modelValue"
      :label="FIELD_LABELS[field]"
      :placeholder="placeholder"
      :error="showError"
      :error-message="RULES[field].message"
      outlined
      dense
      hide-bottom-space
      autocomplete="off"
      class="review-field__control"
      @update:model-value="onUpdate"
      @blur="onBlur"
    />

    <!-- Margin row: the provenance note sits at the line's origin, a filed
         maroon stamp closes the line once the entry passes its rule. The
         stamp stays decorative — Quasar's error messaging remains the only
         announcement, so screen readers hear no new copy. -->
    <div v-if="sourceNote || showDone" class="review-field__foot">
      <p v-if="sourceNote" class="review-field__source">
        {{ sourceNote }}
      </p>
      <span v-if="showDone" class="review-field__stamp" aria-hidden="true">
        <q-icon name="check" size="14px" />
      </span>
    </div>
  </div>
</template>

<style scoped lang="scss">
.review-field {
  margin-bottom: var(--spacing-4);
}

.review-field__control {
  width: 100%;
}

// ---- Ruled entry line -----------------------------------------------------
// The outlined box is struck down to one ruled line the value sits on, with
// the label riding above it as tracked small caps. Focus pairs an amber
// hairline hard against the ink rule (amber vs ink 7.90:1); amber alone on
// paper is 1.73:1 — never.

// Touch floor: the dense default is 40px, --touch-target is 44px. The
// transparent 2px bottom border reserves the hairline slot so claiming the
// line never shifts layout, and holds amber directly under the ink rule the
// :before draws (the pseudo fills the padding box, so both stack flush).
.review-field__control :deep(.q-field__control) {
  border-bottom: var(--border-rule) solid transparent;
  border-radius: 0;
  height: var(--touch-target);
  // Value and label start flush with the line's origin, like writing on
  // ruled paper; the arrow marginal rides the line's end.
  padding: 0;
  transition: border-bottom-color var(--duration-fast) var(--ease-out);
}

// The entry rule itself: reduced to its bottom edge, square-cut.
.review-field__control :deep(.q-field__control:before) {
  border: 0;
  border-bottom: var(--border-hairline) solid var(--color-rule-entry);
  border-radius: 0;
  transition: border-color var(--duration-base) var(--ease-out);
}

.review-field__control :deep(.q-field__control:hover:before) {
  border-bottom-color: var(--color-foreground);
}

// Quasar's boxed focus ring is replaced by the amber hairline below.
.review-field__control :deep(.q-field__control:after) {
  display: none;
}

// Error: the entry rule turns red-stamp, carrying the margin note's ink.
.review-field.review-field--error :deep(.q-field__control:before) {
  border-bottom-color: var(--color-stamp-error);
}

// Claimed (last: focus outranks the error rule when both apply): ink rule
// with the amber hairline flush beneath it — the pair is the focus indicator.
.review-field__control.q-field--focused :deep(.q-field__control) {
  border-bottom-color: var(--color-rule-focus);
}

.review-field__control.q-field--focused :deep(.q-field__control:before) {
  border-bottom-color: var(--color-foreground);
}

// ---- Label ----------------------------------------------------------------
.review-field__control :deep(.q-field__label) {
  color: var(--color-foreground-muted);
}

.review-field__control.q-field--focused :deep(.q-field__label) {
  color: var(--color-foreground);
}

.review-field.review-field--error :deep(.q-field__label) {
  color: var(--color-stamp-error);
}

// ---- Margin note (red stamp) ----------------------------------------------
// Quasar pads the bottom block to match the outlined box; with the box
// struck, messages align flush with the line's origin.
.review-field :deep(.q-field__bottom) {
  padding: 0;
}

// Red-stamp correction note: destructive ink on its tint (5.75:1 measured),
// square-cut frame, no shadow. Full 1px border, never a colored side rail.
.review-field.review-field--error :deep(.q-field__message--error) {
  background: var(--color-stamp-error-bg);
  border: var(--border-hairline) solid var(--color-stamp-error);
  border-radius: 0;
  color: var(--color-stamp-error);
  display: inline-block;
  font-size: var(--text-body);
  font-weight: 700;
  line-height: var(--leading-body);
  margin-top: var(--spacing-2);
  padding: var(--spacing-1) var(--spacing-3);
}

// ---- Foot: provenance + filed stamp ---------------------------------------
.review-field__foot {
  align-items: center;
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-2);
  margin-top: var(--spacing-1);
}

.review-field__source {
  color: var(--color-foreground-muted);
  font-size: var(--text-caption);
  font-style: italic;
  margin: 0;
}

// Filed: maroon rubber stamp closing the line — same treatment as the done
// markers on the ticket strip (maroon on its tint, 9.51:1).
.review-field__stamp {
  align-items: center;
  background: var(--color-stamp-bg);
  border: var(--border-hairline) solid var(--color-stamp);
  border-radius: 0;
  color: var(--color-stamp);
  display: inline-flex;
  flex: none;
  height: 22px;
  justify-content: center;
  line-height: 1;
  // Pushes the stamp to the line's end whether or not a note precedes it.
  margin-left: auto;
  width: 22px;
}

// ---- Browser surfaces -----------------------------------------------------
.review-field__control :deep(.q-field__input) {
  // The caret is maroon ink, not the UA's blue.
  caret-color: var(--color-secondary);
}

.review-field__control :deep(.q-field__input::selection) {
  // Selection takes the amber claim tint; graphite on it stays ≥4.5:1.
  background: var(--color-accent-soft);
  color: var(--color-foreground);
}

// Placeholder only shows while the field is floated (otherwise the label
// itself occupies the line), so scope the tint to that state. `.q-field--float`
// sits on the root next to our class — it must stay in the pre-:deep compound
// or the descendant combinator would never match it.
.review-field__control.q-field--float :deep(.q-field__input::placeholder) {
  color: var(--color-foreground-muted);
}

// Dropdown arrow: muted ink (6.00:1), not Quasar's gray.
.review-field__control :deep(.q-field__append) {
  color: var(--color-foreground-muted);
  height: var(--touch-target);
}
</style>
