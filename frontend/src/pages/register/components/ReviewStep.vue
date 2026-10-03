<script setup lang="ts">
import { computed } from "vue";

import AttachmentUploader from "@/components/AttachmentUploader.vue";
import ConsentCheckbox from "@/components/ConsentCheckbox.vue";
import DocumentPreview from "@/components/DocumentPreview.vue";
import ReviewField from "@/components/ReviewField.vue";
import {
  COLLEGES,
  DEGREE_PROGRAM_SUGGESTIONS,
  YEAR_LEVELS
} from "@/domain/registration";
import type {
  Attachment,
  AttachmentKind,
  ParseMode,
  RegistrationDraft
} from "@/domain/registration";
import { SOURCE_NOTES } from "@/domain/validation";

const props = defineProps<{
  fileName: string;
  mode: ParseMode;
  /** Shared reactive draft — each field writes through its own v-model. */
  draft: RegistrationDraft;
  photo: Attachment | null;
  signature: Attachment | null;
  consent: boolean;
  /** Surfaces field errors once a submit has been attempted. */
  revealErrors: boolean;
  isSubmitting: boolean;
  canSubmit: boolean;
}>();

const emit = defineEmits<{
  submit: [];
  startOver: [];
  attach: [kind: AttachmentKind, attachment: Attachment];
  clear: [kind: AttachmentKind];
  reject: [message: string];
  "update:consent": [value: boolean];
}>();

// The draft holds every field as a string (that is what a text input and the
// backend validator both expect), so the numeric year list is stringified once
// here rather than at the call site.
const YEAR_OPTIONS: readonly string[] = YEAR_LEVELS.map(String);

const sourceNote = computed(() =>
  props.mode === "raster" ? SOURCE_NOTES.raster : SOURCE_NOTES.vector
);
</script>

<template>
  <!-- Step 2 is the slip opened flat: the proof and the entry lines open side
       by side, and the actions close the sheet as a ruled footer. The
       DocketPanel header names this step (register.vue's panel title), and
       the parse-mode chip rides the panel's meta slot — this slip owns only
       its own frame, not its own head. -->
  <div class="review-slip">
    <!-- The form spans both panes so the actions can close the whole slip as
         one ruled footer; novalidate and the submit/reveal wiring are exactly
         as they were. -->
    <q-form novalidate @submit="emit('submit')">
      <div class="review-slip__panes">
        <section class="pane pane--proof">
          <h3 class="pane__title type-eyebrow">Document Preview</h3>
          <DocumentPreview :file-name="fileName" :fields="draft" />
        </section>

        <section class="pane pane--entry">
          <h3 class="pane__title type-eyebrow">Review &amp; Correct</h3>

          <ReviewField
            v-model="draft.student_number"
            field="student_number"
            placeholder="YYYY-XXXXX"
            :source-note="sourceNote"
            :reveal="revealErrors"
          />
          <ReviewField
            v-model="draft.full_name"
            field="full_name"
            :source-note="sourceNote"
            :reveal="revealErrors"
          />
          <!-- Creatable: the prototype offered a <datalist> here, so the
               student may type a program that is not among the suggestions. -->
          <ReviewField
            v-model="draft.degree_program"
            field="degree_program"
            :options="DEGREE_PROGRAM_SUGGESTIONS"
            creatable
            :source-note="sourceNote"
            :reveal="revealErrors"
          />

          <div class="pane__pair">
            <ReviewField
              v-model="draft.college"
              field="college"
              :options="COLLEGES"
              :source-note="sourceNote"
              :reveal="revealErrors"
            />
            <ReviewField
              v-model="draft.year_level"
              field="year_level"
              :options="YEAR_OPTIONS"
              :source-note="sourceNote"
              :reveal="revealErrors"
            />
          </div>

          <ReviewField
            v-model="draft.up_mail"
            field="up_mail"
            placeholder="name@up.edu.ph"
            :source-note="sourceNote"
            :reveal="revealErrors"
          />

          <!-- The sheet's second seam: a strong maroon rule opens the
               attachment block, the same way the ruled footer closes its own
               end. -->
          <h3 class="pane__title pane__title--seam type-eyebrow"
            >Identity Attachments</h3
          >

          <AttachmentUploader
            kind="photo"
            label="Photo (2×2 or recent ID photo)"
            :attachment="photo"
            :invalid="revealErrors && !photo"
            @attach="emit('attach', 'photo', $event)"
            @clear="emit('clear', 'photo')"
            @reject="emit('reject', $event)"
          />

          <AttachmentUploader
            kind="signature"
            label="Signature (on white paper, clear scan or photo)"
            :attachment="signature"
            :invalid="revealErrors && !signature"
            class="pane__slot"
            @attach="emit('attach', 'signature', $event)"
            @clear="emit('clear', 'signature')"
            @reject="emit('reject', $event)"
          />

          <!-- Own wrapper, not a class on the component: ConsentCheckbox
               renders a fragment root, so a class passed to it could not be
               inherited. -->
          <div class="pane__clause">
            <ConsentCheckbox
              :model-value="consent"
              :invalid="revealErrors && !consent"
              @update:model-value="emit('update:consent', $event)"
            />
          </div>
        </section>
      </div>

      <div class="review-slip__actions">
        <q-btn
          unelevated
          color="primary"
          type="submit"
          :label="isSubmitting ? 'Submitting…' : 'Submit Registration'"
          :loading="isSubmitting"
          :disable="!canSubmit"
        />
        <q-btn
          outline
          color="primary"
          label="Start over"
          :disable="isSubmitting"
          @click="emit('startOver')"
        />
      </div>
    </q-form>
  </div>
</template>

<style scoped lang="scss">
// ---- Slip ------------------------------------------------------------------
// The slip's frame: square-cut white paper on hairline edges, drawn here
// because this step's two panes are its own frame. Elevation is declared once —
// the border — so no shadow rides alongside it (AppCard's frame language).
.review-slip {
  background: var(--color-surface);
  border: var(--border-hairline) solid var(--color-rule-hairline);
  border-radius: 0;
}

// Claimed: focus anywhere inside the slip inks the frame and lays the amber
// hairline hard against it — the same pairing AppCard's slip uses (amber vs
// ink 7.90:1; amber alone on paper is 1.73:1, never).
.review-slip:focus-within {
  border-color: var(--color-foreground);
  outline: var(--border-rule) solid var(--color-rule-focus);
  outline-offset: 0;
}

// ---- Two panes -------------------------------------------------------------
// Document proof left, ruled entry lines right. Mobile-first: one stacked
// column until the 900px collapse. Panes stretch (no `start` alignment) so the
// hairline divider always runs the full height of the taller pane.
.review-slip__panes {
  display: grid;
  grid-template-columns: 1fr;
}

.pane {
  min-width: 0;
  padding: var(--spacing-4);
}

// Stacked: the proof pane is ruled off above the entry lines.
.pane--proof {
  border-bottom: var(--border-hairline) solid var(--color-rule-hairline);
}

// ---- Ruled section labels --------------------------------------------------
// Tracked small caps with the rule running out to the pane edge — the ruled
// header every block on a slip opens with, and the label language
// AttachmentUploader already uses above each slot. It heads its block; nothing
// sits above it, so it is the block's own title, not a kicker.
// .type-eyebrow carries the register, matching AttachmentUploader's label;
// this rule keeps the rule-out, the ink, the gap and the margin.
.pane__title {
  align-items: center;
  color: var(--color-secondary); // maroon on paper 10.87:1
  display: flex;
  gap: var(--spacing-2);
  margin: 0 0 var(--spacing-3);
}

.pane__title::after {
  background: var(--color-rule-hairline);
  content: "";
  flex: 1;
  height: var(--border-hairline);
}

// The second seam of the sheet: a strong maroon rule opens the block, with more
// air above the rule than between it and its label.
.pane__title--seam {
  border-top: var(--border-rule) solid var(--color-rule-strong);
  margin-top: var(--spacing-6);
  padding-top: var(--spacing-4);
}

// ---- Entry lines -----------------------------------------------------------
// College + year share one ruled row, two-up only while the pane can hold two
// honest lines. The entry pane is half the sheet's 1100px measure once the
// steps are folded, so there it drops to a line each — the row measures its own
// container, which is why it needs no breakpoint of its own.
.pane__pair {
  display: grid;
  gap: 0 var(--spacing-4);
  grid-template-columns: repeat(auto-fit, minmax(12rem, 1fr));
}

.pane__slot {
  margin-top: var(--spacing-4);
}

.pane__clause {
  margin-top: var(--spacing-6);
}

// The fold is this step's own decision, so the slot rows answer to it here
// rather than in the shared uploader: the paper window, the action and the
// clear stamp are fixed, and on a phone (or in a folded pane) they out-measure
// the row. Letting it wrap keeps the filename and its hint on their own line
// instead of crushing them into a character-wide column.
.pane--entry :deep(.uploader-field .q-field__control-container) {
  flex-wrap: wrap;
}

.pane--entry :deep(.uploader-field .uploader__info) {
  flex: 1 1 12rem;
}

// Touch floor on the slot's clear stamp: dense would put it under 44px.
.pane--entry :deep(.uploader-field .uploader__clear) {
  min-height: var(--touch-target);
}

// ---- Ruled footer ----------------------------------------------------------
// The strong maroon rule closes the sheet and the actions ride beneath it as
// the slip's stamp row, spanning both panes.
.review-slip__actions {
  border-top: var(--border-rule) solid var(--color-rule-strong);
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-3);
  padding: var(--spacing-4);
}

// Both actions are square cells: the filing stamp and the reopen stamp, cut off
// the pill the global bridge would leave. Global .q-btn already carries the
// 44px floor; restated so the target survives a bridge change.
.review-slip__actions :deep(.q-btn) {
  border-radius: 0;
  min-height: var(--touch-target);
}

// Reopen stamp: ruled in ink instead of a second teal outline, so the filled
// filing stamp stays the footer's only stamped cell. `color="primary"` emits
// .text-primary with !important, and .q-btn--outline pins a transparent
// background, so both are out-specified here.
//
// No .type-eyebrow available: this targets a Quasar-internal through :deep(),
// so there is no authored tag to hang the role class on. The register stays
// spelled out here — the same outcome as the .q-btn bridge decision elsewhere.
.review-slip__actions :deep(.q-btn--outline) {
  color: var(--color-foreground) !important; // ink on paper ~12:1
  font-size: var(--text-caption);
  letter-spacing: var(--tracking-eyebrow);
  padding: 0 var(--spacing-6);
  text-transform: uppercase;
}

.review-slip__actions :deep(.q-btn--outline::before) {
  border-color: var(--color-rule-entry);
}

.review-slip__actions :deep(.q-btn--outline:hover::before) {
  border-color: var(--color-foreground);
}

.review-slip__actions :deep(.q-btn--outline:not(.disabled):hover) {
  background: var(--color-surface-sunken) !important;
}

// Claimed: the ruled cell inks its frame so the amber hairline always has ink
// beneath it. Declared after the hover rules so a focused cell that is also
// hovered reads as claimed.
.review-slip__actions :deep(.q-btn--outline:focus-visible::before) {
  border-color: var(--color-foreground);
}

// Claim: the amber hairline rides hard against the button's own edge — 5.96:1
// against the filled teal cell, ink under it on the ruled one. Amber alone on
// paper is 1.73:1, so the ring never carries the state by itself. Same ring the
// OCR gate's action wears; outranks the global :focus-visible teal ring.
.review-slip__actions :deep(.q-btn:focus-visible) {
  border-radius: 0;
  outline: var(--border-rule) solid var(--color-rule-focus);
  outline-offset: 0;
}

@media (min-width: 900px) {
  // The sheet unfurls: proof left, entry lines right, hairline between them.
  .review-slip__panes {
    grid-template-columns: 1fr 1fr;
  }

  .pane {
    padding: var(--spacing-6);
  }

  // Side by side: the hairline turns vertical between the panes.
  .pane--proof {
    border-bottom: 0;
    border-right: var(--border-hairline) solid var(--color-rule-hairline);
  }

  // The footer keeps the panes' inline margins so the sheet's rules and its
  // buttons share one edge; its own padding stays tighter than the panes'.
  .review-slip__actions {
    padding: var(--spacing-4) var(--spacing-6);
  }
}
</style>
