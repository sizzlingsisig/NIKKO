<script setup lang="ts">
import type { FieldKey } from "@/domain/validation";
import type { RegistrationDraft } from "@/domain/registration";

defineProps<{ fileName: string; fields: RegistrationDraft }>();

// A parsed field with no value yet shows as "not extracted" in the facsimile.
// A null-mark would read as a parser failure, and the upload path can genuinely
// leave a field empty (OCR fallback) — this is a recorded state, not an error.
const display = (key: FieldKey, fields: RegistrationDraft) =>
  fields[key] || "not extracted";
</script>

<template>
  <div class="doc-preview">
    <!-- Paper head: the proof's file meta rides a ruled bar in mono, the same
         header block as AppCard but without a filled band. -->
    <div class="doc-preview__bar">
      <span class="doc-preview__filename">{{ fileName }}</span>
      <span class="doc-preview__page-count">Page 1 / 1</span>
    </div>

    <!-- Proof sheet on a sunken-paper stage: elevation declared once, as the
         soft lift — no border riding the shadow. -->
    <div class="doc-preview__page">
      <p class="doc-preview__watermark" aria-hidden="true"
        >UNIVERSITY OF THE PHILIPPINES VISAYAS</p
      >

      <p class="doc-preview__title">UNIVERSITY OF THE PHILIPPINES VISAYAS</p>
      <p class="doc-preview__subtitle">Certificate of Registration, Form 5</p>
      <hr />

      <p>
        Student No.:
        <span class="doc-preview__hl">{{
          display("student_number", fields)
        }}</span>
      </p>
      <p>
        Name:
        <span class="doc-preview__hl">{{ display("full_name", fields) }}</span>
      </p>
      <p>
        College:
        <span class="doc-preview__hl">{{ display("college", fields) }}</span>
        &nbsp; Year:
        <span class="doc-preview__hl">{{ display("year_level", fields) }}</span>
      </p>
      <p>
        Degree Program:
        <span class="doc-preview__hl">{{
          display("degree_program", fields)
        }}</span>
      </p>
      <p>
        UP Mail:
        <span class="doc-preview__hl">{{ display("up_mail", fields) }}</span>
      </p>

      <hr />
      <p class="doc-preview__privacy">
        [ financial assessment, home address &amp; guardian blocks intentionally
        not rendered. Sensitive fields are discarded per privacy policy ]
      </p>
    </div>
  </div>
</template>

<style scoped lang="scss">
// Document window: square-cut frame on the paper stage, hairline edge only
// (the sheet inside carries the elevation).
.doc-preview {
  background: var(--color-surface-sunken);
  border: var(--border-hairline) solid var(--color-rule-hairline);
  border-radius: 0;
  max-height: 34rem; // 544px
  overflow: auto;
}

.doc-preview__bar {
  position: sticky;
  top: 0;
  z-index: 1;
  display: flex;
  justify-content: space-between;
  gap: var(--spacing-3);
  padding: var(--spacing-2) var(--spacing-3);
  // Sticky over the scrolling facsimile, so it carries its own paper ground and
  // a fine rule; the file name and page count are graphite ink on stock.
  background: var(--color-surface);
  border-bottom: var(--border-hairline) solid var(--color-rule-hairline);
  color: var(--color-foreground);
  font-family: var(--font-mono);
  font-size: var(--text-caption);
  font-variant-numeric: tabular-nums;
  line-height: var(--leading-caption);
}

.doc-preview__filename {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.doc-preview__page-count {
  flex: none;
}

.doc-preview__page {
  position: relative;
  width: 92%;
  margin: var(--spacing-4) auto;
  padding: var(--spacing-4);
  background: var(--color-surface);
  color: var(--color-foreground);
  box-shadow: var(--shadow-lg); // elevation once: soft offset lift, no border
  font-size: var(--text-caption);
  line-height: var(--leading-caption);
  overflow: hidden;
}

.doc-preview__watermark {
  position: absolute;
  top: 42%;
  left: 50%;
  transform: translate(-50%, -50%) rotate(-32deg);
  color: oklch(0.3767 0.1396 26.51 / 0.09);
  font-size: var(--text-title);
  font-weight: 800;
  white-space: nowrap;
  pointer-events: none;
}

.doc-preview__title {
  color: var(--color-secondary);
  font-weight: 700;
  text-align: center;
}

.doc-preview__subtitle {
  font-size: var(--text-caption);
  text-align: center;
}

// Maroon ruled line — the slip's strong rule, letterhead style.
.doc-preview__page hr {
  border: 0;
  border-top: var(--border-rule) solid var(--color-rule-strong);
  margin: var(--spacing-3) 0;
}

// Parsed proof: the accent underlines the extracted value (graphite on the
// amber tint is AAA; the underline is emphasis, not a control boundary).
.doc-preview__hl {
  background: var(--color-accent-soft);
  border-bottom: var(--border-rule) solid var(--color-accent);
  border-radius: 0;
  font-weight: 700;
  padding: 0 2px;
  word-break: break-word;
}

.doc-preview__privacy {
  color: var(--color-foreground-muted);
  font-size: var(--text-caption);
}

@media (min-width: 768px) {
  .doc-preview__bar {
    padding: var(--spacing-3) var(--spacing-4);
  }

  .doc-preview__page {
    padding: var(--spacing-6);
    width: 88%;
  }
}
</style>
