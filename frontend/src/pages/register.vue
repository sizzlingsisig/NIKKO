<script setup lang="ts">
import { computed, reactive, ref } from "vue";
import { useQuasar } from "quasar";

import AppChip from "@/components/AppChip.vue";
import { MOCK_VECTOR, renameSource } from "@/domain/mockData";
import type { ParsedForm5 } from "@/domain/registration";
import {
  EMPTY_DRAFT,
  type Attachment,
  type AttachmentKind,
  type RegistrationDraft
} from "@/domain/registration";
import { formatBytes } from "@/domain/roster";
import { MAX_PDF_BYTES } from "@/domain/validation";

import DocketPanel from "./register/components/DocketPanel.vue";
import DoneStep from "./register/components/DoneStep.vue";
import GuidelinesCard from "./register/components/GuidelinesCard.vue";
import OcrConfidenceDialog from "./register/components/OcrConfidenceDialog.vue";
import PrivacyCard from "./register/components/PrivacyCard.vue";
import RegisterWorkspace from "./register/components/RegisterWorkspace.vue";
import ReviewStep from "./register/components/ReviewStep.vue";
import StepOverviewCard from "./register/components/StepOverviewCard.vue";
import UploadStep from "./register/components/UploadStep.vue";
import { useForm5Parse } from "./register/composables/useForm5Parse";
import { useRegistrationSubmit } from "./register/composables/useRegistrationSubmit";

const $q = useQuasar();

// Wizard state: which step, the last parse result, and the draft the student
// edits — everything else (parse timers, submit lifecycle) lives in the
// colocated composables under ./register/composables.
const step = ref(0);
const parsed = ref<ParsedForm5 | null>(null);
const draft = reactive<RegistrationDraft>({ ...EMPTY_DRAFT });
const photo = ref<Attachment | null>(null);
const signature = ref<Attachment | null>(null);
const consent = ref(false);
const revealErrors = ref(false);
const referenceId = ref("");
const ocrDialogOpen = ref(false);

// PhaseStrip exposes no cancelable transition event, so navigation is
// guarded declaratively: a cell stays a control only for steps this run has
// actually visited, and the receipt page locks the strip outright — its
// parse result has been released there, so Review would render empty.
const maxReached = ref(0);
const finished = ref(false);

function reached(name: number): boolean {
  return !finished.value && name <= maxReached.value;
}

// ---- Pinned per-step copy (spec §6.2–6.4) ----------------------------------
// The docket title, the sidebar briefing and the guidelines checklist all
// read one index: the current step. `as const` keeps each table a tuple (and
// each entry defined), which is what lets noUncheckedIndexedAccess accept
// the ?? fallbacks below.

const PANEL_TITLES = [
  "Upload Form 5 PDF",
  "Verify Student Data",
  "Issuance & Confirmation"
] as const;

const OVERVIEWS = [
  {
    eyebrow: "— STEP 01 / OVERVIEW",
    title: "Matriculation Verification",
    body: "Provide your official UP Form 5 (Electronic or Scanned PDF). Runs entirely inside your browser — your Form 5 never leaves this device."
  },
  {
    eyebrow: "— STEP 02 / OVERVIEW",
    title: "Verify Student Data",
    body: "Review the roster fields extracted from your Form 5, attach your photo and signature, and confirm RA 10173 consent."
  },
  {
    eyebrow: "— STEP 03 / OVERVIEW",
    title: "Issuance & Confirmation",
    body: "Your registration has been recorded. Keep the reference ID below as your proof of submission."
  }
] as const;

const GUIDELINES_VARIANTS = ["upload", "review", "next"] as const;

const panelTitle = computed(() => PANEL_TITLES[step.value] ?? PANEL_TITLES[0]);
const overview = computed(() => OVERVIEWS[step.value] ?? OVERVIEWS[0]);
const guidelinesVariant = computed(
  () => GUIDELINES_VARIANTS[step.value] ?? "upload"
);

// Step 02's meta tally: how many of the draft's fields hold something the
// student can see (trimmed, so a stray space does not count as filled).
const filledCount = computed(() => {
  const total = Object.keys(draft).length;
  const fields: [string, string][] = Object.entries(draft);
  const nonEmpty = fields.filter(([, value]) => value.trim() !== "").length;
  return `${nonEmpty}/${total}`;
});

// The parse-mode stamp that rode ReviewStep's head — moved to the panel's
// meta slot when the docket header superseded that head (spec §6.4).
const parseChip = computed(() =>
  parsed.value?.mode === "raster"
    ? { label: "OCR FALLBACK", tone: "caution" as const }
    : { label: "TEXT-LAYER PARSE", tone: "positive" as const }
);

function notify(message: string) {
  $q.notify({ message, color: "dark", position: "bottom", timeout: 3400 });
}

const { logLines, isParsing, runParse, resetParse } =
  useForm5Parse(enterReview);

const { isSubmitting, canSubmit, onSubmit, releaseSubmission, resetSubmit } =
  useRegistrationSubmit({
    draft,
    photo,
    signature,
    consent,
    revealErrors,
    notify,
    onSubmitted: value => {
      referenceId.value = value;
      step.value = 2;
      maxReached.value = 2;
      finished.value = true;
      // FR-2.4: drop every trace of this submission from the page.
      releaseVolatileData();
    }
  });

function enterReview(payload: ParsedForm5) {
  parsed.value = payload;
  Object.assign(draft, payload.fields);
  revealErrors.value = false;

  // No fabricated attachments: the student attaches their own 2x2 photo and
  // signature in step 2, which is what the submission contract requires. A
  // real registration must never ship a stand-in.

  // The raster payload currently has no entry point (real uploads replay the
  // text-layer simulation); the gate stays wired for when OCR lands.
  if (payload.mode === "raster") {
    ocrDialogOpen.value = true;
  }

  // Parse no longer advances the wizard (spec §6.4): the payload lands here
  // while the student is still on step 0. CONTINUE TO STEP 02 (onContinue)
  // is what moves them on.
}

function onFileAccepted(file: File) {
  // No pdfjs-dist yet: any accepted PDF replays the text-layer simulation
  // payload under the student's own filename.
  void runParse(renameSource(MOCK_VECTOR, file.name));
}

function onAttach(kind: AttachmentKind, attachment: Attachment) {
  if (kind === "photo") photo.value = attachment;
  else signature.value = attachment;
}

function onClearAttachment(kind: AttachmentKind) {
  const current = kind === "photo" ? photo.value : signature.value;
  if (current?.url.startsWith("blob:")) URL.revokeObjectURL(current.url);
  if (kind === "photo") photo.value = null;
  else signature.value = null;
}

/** FR-2.4: clear the submission payload, the parse result and its log. */
function releaseVolatileData() {
  releaseSubmission();
  parsed.value = null;
  resetParse();
}

function startOver() {
  releaseVolatileData();
  resetSubmit();
  ocrDialogOpen.value = false;
  step.value = 0;
  maxReached.value = 0;
  finished.value = false;
}

/** Step 02's gate: only a settled parse opens the review docket. */
function onContinue() {
  if (!parsed.value || isParsing.value) return;
  step.value = 1;
  maxReached.value = Math.max(maxReached.value, 1);
}

/** PhaseStrip renders unreachable cells as spans; this is the belt. */
function onJump(i: number) {
  if (reached(i)) step.value = i;
}

// The guidelines card is the "GUIDELINES & FAQ" button's target: scroll it
// into view, then focus the card itself — tabindex="-1" falls through its
// single root from the template below, so focus lands without adding a tab
// stop.
const guidelines = ref<InstanceType<typeof GuidelinesCard> | null>(null);

function focusGuidelines() {
  guidelines.value?.$el?.scrollIntoView({
    behavior: "smooth",
    block: "nearest"
  });
  (guidelines.value?.$el as HTMLElement | undefined)?.focus({
    preventScroll: true
  });
}
</script>

<template>
  <!-- The document workspace: RegisterWorkspace lays the bar, the phase strip
       and the sidebar/panel columns; the sidebar carries the briefing cards
       and the docket panel carries whichever step slip is standing. The step
       components keep their v-if chain and every prop/emits binding exactly
       as it was — only the frame around them is new, and PhaseStrip's
       reachability gate is reinforced by onJump's guard. -->
  <div class="register-shell">
    <RegisterWorkspace
      :step="step"
      :max-reached="maxReached"
      :finished="finished"
      @jump="onJump"
    >
      <template #sidebar>
        <StepOverviewCard :eyebrow="overview.eyebrow" :title="overview.title">
          {{ overview.body }}
          <template #status>
            <template v-if="step === 0">
              <span class="status-row">
                <span class="status-row__label">PARSER ENGINE</span>
                <span class="status-row__value">FORM5-PARSER · SIM v1.8.4</span>
              </span>
              <span class="status-pill">
                <span class="status-pill__dot" aria-hidden="true">●</span>
                {{ isParsing ? "PARSING" : "READY" }}
              </span>
            </template>
            <span v-else-if="step === 1" class="status-row">
              <span class="status-row__label">FIELDS EXTRACTED</span>
              <span class="status-row__value">{{ filledCount }}</span>
            </span>
            <span v-else class="status-row">
              <span class="status-row__label">REFERENCE ID</span>
              <span class="status-row__value">{{ referenceId }}</span>
            </span>
          </template>
        </StepOverviewCard>

        <PrivacyCard />

        <GuidelinesCard
          ref="guidelines"
          tabindex="-1"
          :variant="guidelinesVariant"
        />
      </template>

      <template #panel>
        <DocketPanel eyebrow="DOCKET FORM 5-A" :title="panelTitle">
          <template #meta>
            <span v-if="step === 0">
              MAX SIZE: {{ formatBytes(MAX_PDF_BYTES) }}
            </span>
            <span v-else-if="step === 1" class="panel-meta">
              <AppChip :label="parseChip.label" :tone="parseChip.tone" />
              <span>{{ filledCount }}</span>
            </span>
            <span v-else-if="step === 2">REF ID · {{ referenceId }}</span>
          </template>

          <UploadStep
            v-if="step === 0"
            :is-parsing="isParsing"
            :log-lines="logLines"
            @accept="onFileAccepted"
            @reject="notify"
          />

          <ReviewStep
            v-else-if="step === 1 && parsed"
            :file-name="parsed.fileName"
            :mode="parsed.mode"
            :draft="draft"
            :photo="photo"
            :signature="signature"
            :consent="consent"
            :reveal-errors="revealErrors"
            :is-submitting="isSubmitting"
            :can-submit="canSubmit"
            @submit="onSubmit"
            @start-over="startOver"
            @attach="onAttach"
            @clear="onClearAttachment"
            @reject="notify"
            @update:consent="consent = $event"
          />

          <DoneStep
            v-else-if="step === 2"
            :ref-id="referenceId"
            @restart="startOver"
          />

          <template v-if="step === 0" #actions>
            <q-btn
              unelevated
              color="primary"
              label="CONTINUE TO STEP 02"
              :disable="!parsed || isParsing"
              @click="onContinue"
            />
            <q-btn outline label="GUIDELINES & FAQ" @click="focusGuidelines" />
          </template>
        </DocketPanel>
      </template>
    </RegisterWorkspace>

    <OcrConfidenceDialog
      :model-value="ocrDialogOpen"
      @update:model-value="ocrDialogOpen = $event"
    />
  </div>
</template>

<style scoped lang="scss">
// The shell: RegisterWorkspace brings the workspace grid (bar, phase strip,
// sidebar, panel) inside it, and the OCR gate rides as its sibling. min-width
// 0 keeps this block from being sized past its track by a long unbreakable
// string inside either column.
.register-shell {
  min-width: 0;
}

// ---- Sidebar status box ----------------------------------------------------
// The overview card's machine readout (spec §6.2): mono rows in the box's
// caption type, label muted at the left and value ink at the right — the
// privacy card's footer split — then the parser pill: a square cell ruled in
// the control ink, its ● dot in pine-teal (10.33:1 on paper; the word
// carries the state, the dot only lights it). No ERROR state exists:
// useForm5Parse has no failure path (documented deviation from spec §6.2,
// honest per D3).
.status-row {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-1) var(--spacing-3);
}

.status-row__label {
  color: var(--color-foreground-muted); // 6.00:1 on paper
}

.status-row__value {
  color: var(--color-foreground); // 13.69:1 on paper
  margin-left: auto;
  text-align: right;
}

// Shrink to its own label: the status grid would otherwise stretch the cell
// across the box, turning the pill into a bar.
.status-pill {
  border: var(--border-hairline) solid var(--color-rule-entry);
  color: var(--color-foreground);
  justify-self: start;
  padding: var(--spacing-1) var(--spacing-2);
}

.status-pill__dot {
  color: var(--color-primary); // pine-teal dot, 10.33:1 on paper
}

// Step 02's meta: the parse-mode chip beside the field tally, one line in
// the docket header. inline-flex so the chip (a Quasar box) and the count
// share the row no matter which of them turns out to be a block.
.panel-meta {
  align-items: center;
  display: inline-flex;
  gap: var(--spacing-2);
}
</style>
