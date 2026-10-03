<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{ refId: string }>();
const emit = defineEmits<{ restart: [] }>();

// The stub reads its own state off the reference id: an empty id means the
// atomic commit has not landed yet, so the stamp block renders drawn-but-not-
// struck. Both states ship inside the one component — no prop added.
const isStruck = computed(() => props.refId.trim().length > 0);
</script>

<template>
  <div class="ack">
    <!-- Submitting: the stamp frame in pending ink with the spinner where the
         mark will land. role="status" announces the state as it changes. -->
    <div v-if="!isStruck" class="ack__stamp ack__stamp--pending" role="status">
      <q-spinner size="16px" aria-hidden="true" />
      <span class="ack__pending-label type-eyebrow">Submitting…</span>
    </div>

    <template v-else>
      <!-- Rubber stamp: square block ruled twice in its own ink, struck a
           degree off-square over the straight counterfoil lines below. The
           double hairline is the edge — no shadow rides with it. -->
      <div class="ack__stamp ack__stamp--struck">
        <q-icon name="check_circle" class="ack__mark" aria-hidden="true" />
        <h2 class="ack__title">Registration received</h2>
      </div>

      <p class="ack__ref" :aria-label="`Reference ID ${refId}`">{{ refId }}</p>

      <p class="ack__lede">
        Your record has been written to the organization roster. Save your
        reference ID. It is the only confirmation you will receive.
      </p>
      <p class="ack__note">
        Simulated atomic response: acknowledgement + reference ID only. No
        stored records are ever returned by the API (FR-3.4).
      </p>

      <q-btn
        outline
        color="primary"
        label="Register another member"
        class="ack__restart"
        @click="emit('restart')"
      />
    </template>
  </div>
</template>

<style scoped lang="scss">
.ack {
  padding: var(--spacing-6) var(--spacing-4);
  text-align: center;
}

// Shared stamp geometry: square block ruled in its own ink, with the second
// hairline ruled inside it. Both rules stay 1px — the double rule is the
// stamp's edge, elevation declared once.
.ack__stamp {
  background: var(--color-stamp-bg);
  border: var(--border-hairline) solid var(--color-stamp);
  color: var(--color-stamp); // maroon on its tint 9.51:1
  display: inline-block;
  margin-top: var(--spacing-2);
  max-width: 100%;
  padding: var(--spacing-4) var(--spacing-6);
  position: relative;
  text-align: center;
}

.ack__stamp::before {
  border: var(--border-hairline) solid currentColor;
  content: "";
  inset: var(--spacing-2);
  pointer-events: none;
  position: absolute;
}

// Struck — the one authored moment of this stub: the stamp lands a couple of
// degrees off-square. Static, no animation, no fake delay.
.ack__stamp--struck {
  transform: rotate(-2deg);
}

.ack__mark {
  // Stays inline-flex (Quasar's own box) so the glyph self-centers in a box
  // that is as tall as its 40px mark; the parent centers it on the line.
  color: inherit;
  font-size: var(--text-title);
  margin: 0 0 var(--spacing-2);
}

// Not yet struck: unstamped stock, pending ink, spinner in the mark's place.
// Same frame as the struck stamp, so nothing about the block changes but the
// ink and what it carries. T8: min-height here is a dimension, not a spacing
// step — 4rem is --size-ack.
.ack__stamp--pending {
  align-items: center;
  background: var(--color-surface-sunken);
  border-color: var(--color-stamp-pending);
  color: var(--color-stamp-pending); // muted on this stock 5.30:1
  display: inline-flex;
  gap: var(--spacing-3);
  min-height: var(--size-ack);
  padding: var(--spacing-4) var(--spacing-8);
}

// The heading IS the mark: tracked caps stamped in its own ink. No kicker
// line above it — the mark carries its own weight. No role class: this is a
// subhead-sized tracked caps, where .type-subhead has no tracking/uppercase
// and .type-eyebrow would drop it to caption. Register stays spelled out.
.ack__title {
  color: inherit;
  font-size: var(--text-subhead);
  font-weight: var(--weight-bold);
  letter-spacing: var(--tracking-eyebrow);
  line-height: var(--leading-tight);
  margin: 0;
  text-transform: uppercase;
}

// The counterfoil number: mono because it is data the student copies, ruled
// top and bottom like the stub line it sits on. Ink on paper 13.69:1.
.ack__ref {
  border-top: var(--border-hairline) solid var(--color-rule-entry);
  border-bottom: var(--border-hairline) solid var(--color-rule-entry);
  color: var(--color-foreground);
  display: block;
  font-family: var(--font-mono);
  // Large, but capped so REG-YYYY-NNNNN never outgrows a 375px screen.
  font-size: var(--text-title-fluid);
  font-weight: var(--weight-bold);
  // Tracking snapped 0.1em -> --tracking-normal (VISIBLE). This is the value
  // itself, not an uppercase label, so the brief's rule lands it on normal —
  // which also matches .type-data, the token system's own mono role, and
  // carries no letter-spacing. Flagged in the report: the old 0.1em gave the
  // code visible glyph separation, so a human may prefer --tracking-eyebrow.
  letter-spacing: var(--tracking-normal);
  margin: var(--spacing-6) auto var(--spacing-4);
  max-width: 100%;
  overflow-wrap: anywhere;
  padding: var(--spacing-3) var(--spacing-2);
}

.ack__lede {
  color: var(--color-foreground);
  font-size: var(--text-body);
  line-height: var(--leading-body);
  margin: 0 auto;
  max-width: 34rem;
}

.ack__note {
  color: var(--color-foreground-muted);
  font-size: var(--text-caption);
  line-height: var(--leading-caption);
  margin: var(--spacing-3) auto 0;
  max-width: 34rem;
}

.ack__restart {
  margin-top: var(--spacing-6);
}

@media (min-width: 768px) {
  .ack__stamp {
    padding: var(--spacing-4) var(--spacing-8);
  }
}
</style>
