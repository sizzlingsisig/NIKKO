<script setup lang="ts">
import { formatBytes } from "@/domain/roster";
import type { Attachment, AttachmentKind } from "@/domain/registration";
import { isImage, MAX_IMAGE_BYTES } from "@/domain/validation";

const props = defineProps<{
  kind: AttachmentKind;
  label: string;
  attachment: Attachment | null;
  /** Surfaces the "required" error once a submit has been attempted. */
  invalid: boolean;
}>();

const emit = defineEmits<{
  attach: [attachment: Attachment];
  clear: [];
  reject: [message: string];
}>();

const LABEL = { photo: "Photo", signature: "Signature" } as const;
const PLACEHOLDER_TEXT = {
  photo: "No photo attached",
  signature: "No signature attached"
} as const;

const ERROR_SUFFIX = {
  photo: " for the membership record",
  signature: ""
} as const;

/**
 * The payload is a plain `File[]`; Quasar does not declare `onAdd` on
 * `QFileProps`, so the annotation here is the contract we rely on. QFile is
 * kept uncontrolled (`:model-value="null"`) — the preview lives in
 * `attachment`, which the page owns once this emits.
 */
function onAdd(files: readonly File[]) {
  const picked = files[0];
  // QFile's own `accept` filter drops non-matching files silently, which
  // would swallow the message below. Validate here so the student is told.
  if (picked && !isImage(picked.type)) {
    emit("reject", "Only image files (JPG/PNG) are accepted.");
  } else if (picked && picked.size > MAX_IMAGE_BYTES) {
    emit("reject", `${LABEL[props.kind]} exceeds the 2 MB limit.`);
  } else if (picked) {
    // Object URL, not a data URL: the browser releases the bytes on revoke,
    // which is what FR-2.4 asks for once the submission completes.
    emit("attach", {
      name: picked.name,
      size: picked.size,
      url: URL.createObjectURL(picked)
    });
  }
}
</script>

<template>
  <div class="uploader-field" :class="{ 'uploader-field--invalid': invalid }">
    <span class="uploader-field__label">{{ label }}</span>

    <q-file
      dropzone
      borderless
      class="uploader"
      :class="{
        'uploader--filled': attachment,
        'uploader--invalid': invalid
      }"
      :model-value="null"
      :aria-label="`${attachment ? 'Replace' : 'Attach'} ${LABEL[kind].toLowerCase()}`"
      @add="onAdd"
    >
      <q-avatar
        square
        class="uploader__thumb"
        :class="{ 'uploader__thumb--sig': kind === 'signature' }"
      >
        <img
          v-if="attachment"
          :src="attachment.url"
          :alt="`${kind} preview`"
          loading="lazy"
        />
        <q-icon v-else-if="kind === 'photo'" name="image" aria-hidden="true" />
        <q-icon v-else name="draw" aria-hidden="true" />
      </q-avatar>

      <span class="uploader__info">
        <span
          class="uploader__name"
          :class="{ 'uploader__name--filed': attachment }"
          >{{ attachment?.name ?? PLACEHOLDER_TEXT[kind] }}</span
        >
        <span class="uploader__hint">
          <template v-if="attachment"
            >{{ formatBytes(attachment.size) }}, </template
          >JPG / PNG, max 2 MB, preview only — kept in this browser and released
          after submission
        </span>
      </span>

      <span class="uploader__action">{{
        attachment ? "Replace" : "Attach"
      }}</span>
      <q-btn
        v-if="attachment"
        round
        flat
        dense
        class="uploader__clear"
        :aria-label="`Remove ${kind}`"
        @click.stop="emit('clear')"
      >
        <q-icon name="close" aria-hidden="true" />
      </q-btn>
    </q-file>

    <p v-if="invalid" class="uploader-field__error" role="alert">
      A {{ LABEL[kind].toLowerCase() }} is required{{ ERROR_SUFFIX[kind] }}.
    </p>
  </div>
</template>

<style scoped lang="scss">
// Field label on its ruled line: tracked small caps with the rule running to
// the edge — the ruled-entry header language of the slip.
.uploader-field__label {
  align-items: center;
  color: var(--color-foreground-muted);
  display: flex;
  font-size: var(--text-caption);
  font-weight: 700;
  gap: var(--spacing-2);
  letter-spacing: var(--tracking-eyebrow);
  margin-bottom: var(--spacing-2);
  text-transform: uppercase;
}

.uploader-field__label::after {
  background: var(--color-rule-hairline);
  content: "";
  flex: 1;
  height: var(--border-hairline);
}

// Error: the ruled label inks red alongside the frame and margin note.
.uploader-field--invalid .uploader-field__label {
  color: var(--color-stamp-error); // 6.57:1 on paper
}

// The default slot is rendered inside `.q-field__control-container`, which
// Quasar lays out as a `row no-wrap` flex box — exactly what this compact
// thumb / info / action row needs. `borderless` drops the `q-field--standard`
// variant, whose `:after` would otherwise draw a stray bottom rule under the
// box; the box itself is drawn here. The layout fix that lets the slot span
// the full width lives in app.scss.
//
// The box is an attachment slot on the slip: sunken stock with a dashed
// hairline waiting to be filled (rule-entry is the 3.48:1 boundary; the
// decorative hairline never guards a control).
.uploader {
  width: 100%;

  :deep(.q-field__control) {
    min-height: 0;
    padding: 0;
  }

  :deep(.q-field__control-container) {
    align-items: center;
    background: var(--color-surface-sunken);
    border: var(--border-hairline) dashed var(--color-rule-entry);
    border-radius: 0;
    display: flex;
    gap: var(--spacing-4);
    text-align: left;
    transition:
      border-color var(--duration-base) var(--ease-out),
      background var(--duration-base) var(--ease-out);
    // Same mechanism as Form5Dropzone: nowrap row shrink-wraps slot content.
    width: 100%;
    padding: var(--spacing-3);
  }
}

// Hover on an empty slot: paper warms and the dashes ink in maroon. Excludes
// the claim states so hover never out-ranks drag/focus (its :not() chain gives
// it the highest specificity in this block). The chain must stay on ONE line:
// a newline between :not() pseudos compiles as a descendant combinator and
// silently breaks the selector — only the :deep() part may start a new line.
.uploader:not(.uploader--filled):not(.uploader--invalid):not(.q-file--dnd):not(
    :focus-within
  ):hover
  :deep(.q-field__control-container) {
  background: var(--color-surface);
  border-color: var(--color-rule-strong);
}

// Filed: rubber stamp — maroon on its tint (9.51:1), solid rule where the
// empty slot dashed.
.uploader--filled :deep(.q-field__control-container) {
  background: var(--color-stamp-bg);
  border-color: var(--color-stamp);
  border-style: solid;
}

// Error: paper stays white so the red-stamp margin note reads against it
// (the note itself is the primary signal, per "error = margin note").
.uploader--invalid :deep(.q-field__control-container) {
  background: var(--color-surface);
  border-color: var(--color-stamp-error);
  border-style: solid;
}

// Focus (AppCard's claim frame): ink hairline with the amber hairline hard
// against it — amber vs ink 7.90:1. The outline rides the component root
// because `.q-field__control` clips its children (overflow: hidden).
.uploader:focus-within {
  outline: var(--border-rule) solid var(--color-rule-focus);
  outline-offset: 0;
}

.uploader:focus-within :deep(.q-field__control-container) {
  border-color: var(--color-foreground);
  border-style: solid;
}

// QFile marks the root `.q-file--dnd` while a file is over it: the slot is
// claimed — amber paper lit inside the ink frame. Declared last so it wins
// over hover/focus/filled backgrounds while a drag is over the box.
.uploader.q-file--dnd {
  outline: var(--border-rule) solid var(--color-rule-focus);
  outline-offset: 0;
}

.uploader.q-file--dnd :deep(.q-field__control-container) {
  background: var(--color-accent-soft); // graphite on tint 12.4:1
  border-color: var(--color-foreground);
  border-style: solid;
}

// Photo window: square-cut, hairline-framed like every other paper edge in
// the slip (q-avatar `square` handles the radius).
.uploader__thumb {
  background: var(--color-surface);
  border: var(--border-hairline) solid var(--color-rule-entry);
  color: var(--color-foreground-muted);
  flex: none;
  height: var(--spacing-16);
  overflow: hidden;
  width: var(--spacing-16);
}

.uploader__thumb--sig {
  width: 96px;
}

.uploader__thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.uploader__thumb--sig img {
  object-fit: contain;
}

.uploader__info {
  flex: 1;
  min-width: 0;
}

// Empty slot reads pending (5.32:1 on the sunken box); the filed filename
// inks in — mono, because a filename is data.
.uploader__name {
  color: var(--color-stamp-pending);
  display: block;
  font-size: var(--text-body);
  font-weight: 700;
  word-break: break-all;
}

.uploader__name--filed {
  color: var(--color-foreground);
  font-family: var(--font-mono);
  font-variant-numeric: tabular-nums;
}

.uploader__hint {
  color: var(--color-foreground-muted);
  display: block;
  font-size: var(--text-caption);
  line-height: var(--leading-caption);
}

// The stamped action: maroon, underlined hard against its rule.
.uploader__action {
  color: var(--color-secondary);
  flex: none;
  font-size: var(--text-body);
  font-weight: 700;
  text-decoration: underline;
  text-decoration-color: var(--color-rule-strong);
  text-decoration-thickness: var(--border-hairline);
  text-underline-offset: var(--spacing-1);
}

.uploader__clear {
  color: var(--color-foreground-muted);
  flex: none;
}

// Red-stamp margin note: rubber-stamped slip line under the slot. Sentence
// case kept so the error stays plainly readable.
.uploader-field__error {
  background: var(--color-stamp-error-bg);
  border: var(--border-hairline) solid var(--color-stamp-error);
  color: var(--color-stamp-error); // on tint 5.75:1
  font-size: var(--text-body);
  font-weight: 700;
  line-height: var(--leading-body);
  margin: var(--spacing-2) 0 0;
  padding: var(--spacing-2) var(--spacing-3);
}
</style>
