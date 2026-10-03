<script setup lang="ts">
import type { LogLine } from "@/domain/mockData";

defineProps<{ lines: readonly LogLine[] }>();

const BULLETS: Readonly<Record<LogLine["tone"], string>> = {
  ok: "✓",
  warn: "!",
  dim: "—",
  pending: ""
};
</script>

<template>
  <!-- Always rendered: the live region must exist before lines arrive or
       screen readers miss the stream, and the reserved height keeps the
       first line from shoving the slip's controls down.

       `aria-label` names the region: an unnamed `role="log"` is announced as a
       bare "log" with no indication that what it narrates is this file's
       on-device parse. The label is static because the region's purpose never
       changes — only its contents do. -->
  <div
    class="parse-log"
    role="log"
    aria-label="On-device parse log"
    aria-live="polite"
    aria-atomic="false"
  >
    <p
      v-for="(line, index) in lines"
      :key="index"
      class="parse-log__line"
      :class="`parse-log__line--${line.tone}`"
    >
      <!-- QSpinner inherits `currentColor`, so the tone classes below drive it. -->
      <span
        v-if="line.tone === 'pending'"
        class="parse-log__spinner"
        aria-hidden="true"
      >
        <q-spinner size="14px" />
      </span>
      <span v-else class="parse-log__bullet" aria-hidden="true">{{
        BULLETS[line.tone]
      }}</span>
      <span class="parse-log__text">{{ line.text }}</span>
    </p>
  </div>
</template>

<style scoped lang="scss">
// Counter log: the on-device parse stream printed as a ruled strip on the
// slip — sunken stock ruled off top and bottom, every entry on its own ledger
// line. Mono is sanctioned here: the lines are real streaming data (timings,
// regexes, file names), never costume.
.parse-log {
  background: var(--color-surface-sunken);
  // Strong maroon rule marks where the log section starts; a hairline closes
  // it against the paper below. Both are horizontal ruled lines.
  border-top: var(--border-rule) solid var(--color-rule-strong);
  border-bottom: var(--border-hairline) solid var(--color-rule-hairline);
  color: var(--color-foreground); // ink on stock ~12:1
  font-family: var(--font-mono);
  font-size: var(--text-body);
  // Tabular figures keep ms counts from shivering as the stream advances.
  font-variant-numeric: tabular-nums;
  line-height: var(--leading-body);
  // Reserves the stream's height up front, so lines landing never shift the
  // dropzone or buttons above.
  min-height: 150px;
  margin-top: var(--spacing-6);
  padding: var(--spacing-4);
}

.parse-log__line {
  align-items: baseline;
  border-bottom: var(--border-hairline) solid var(--color-rule-hairline);
  display: flex;
  gap: var(--spacing-2);
  margin: 0;
  padding: var(--spacing-1) 0;
}

.parse-log__line:last-child {
  border-bottom: 0;
}

// Long regexes and paths wrap inside the strip instead of clipping it.
.parse-log__text {
  flex: 1;
  min-width: 0;
  overflow-wrap: anywhere;
}

.parse-log__bullet {
  flex: none;
  font-weight: var(--weight-bold);
  width: 1ch;
}

// Filed: the done mark in stamp ink — maroon on stock ~9.7:1.
.parse-log__line--ok .parse-log__bullet {
  color: var(--color-stamp);
}

// Caution: graphite on the amber wash, edge in ink — the same claim cell as
// the active step code. Amber alone on stock is 1.73:1, so the hue never
// carries the mark by itself.
.parse-log__line--warn .parse-log__bullet {
  align-self: center;
  background: var(--color-accent-soft);
  border: var(--border-hairline) solid var(--color-foreground);
  color: var(--color-foreground); // graphite on amber-soft 11.8-12.4:1
  display: inline-grid;
  height: 1.25rem;
  line-height: 1;
  place-items: center;
  width: 1.25rem;
}

// Draft chatter runs muted — 5.30:1 on this stock.
.parse-log__line--dim {
  color: var(--color-stamp-pending);
}

// In-flight line: brand-ink spinner (9.18:1 on stock), text stays ink.
.parse-log__spinner {
  align-self: center;
  color: var(--color-primary);
  display: inline-flex;
  flex: none;
}

@media (min-width: 768px) {
  .parse-log {
    padding: var(--spacing-4) var(--spacing-6);
  }
}
</style>
