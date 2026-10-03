<script setup lang="ts">
import StepAck from "@/components/StepAck.vue";

defineProps<{ refId: string }>();

const emit = defineEmits<{ restart: [] }>();
</script>

<template>
  <!-- Step 3 is the tear-off stub: the docket header (eyebrow + title + REF ID
       meta) rides above the perforation on the panel itself, everything below
       the line is the part the student keeps. StepAck carries every word on
       this screen — this component owns the tear, and nothing else. -->
  <div class="stub">
    <!-- Perforated edge bled to the panel's hairlines so the dashes read as
         one continuous tear line, not a rule floating in the body gutter.
         The tear keeps its own paper gap under the slip band: the band's
         closing maroon rule and the perforation are two different edges,
         and stacking them flush would read as one muddy seam. -->
    <div class="stub__tear" aria-hidden="true">
      <q-icon name="content_cut" class="stub__tear-mark" />
    </div>

    <!-- StepAck is the stub's whole body. The panel body already supplies the
         margin (spacing-6 mobile / spacing-8 desktop — DocketPanel's own body
         rhythm), so StepAck's own padding is handed back — otherwise the two
         stack and the stamp floats in a bordered box inside a bordered box.
         The stub reads as one sheet: header, tear, then the kept portion. -->
    <StepAck class="stub__ack" :ref-id="refId" @restart="emit('restart')" />
  </div>
</template>

<style scoped lang="scss">
// The tear line spans the whole panel: the negative inline margins mirror
// DocketPanel's body padding (spacing-6, spacing-8 from 768px — the exact
// breakpoint DocketPanel itself switches on), so the dashes stop at the
// panel's border instead of inside its gutter. The left padding insets the
// cut mark off that border; border-top is drawn on the padding box, so the
// dashes still run edge to edge.
.stub__tear {
  border-top: var(--border-perforation);
  display: flex;
  margin: 0 calc(-1 * var(--spacing-6)) var(--spacing-6);
  padding-left: var(--spacing-2);
}

// The cut mark rides the line: its paper ground punches a gap in the dashes
// behind it, so the perforation reads as interrupted by the blade. Static —
// StepAck's −2° strike is the only authored motion this step gets. Parked at
// half its own height plus the 1px border, which centres the glyph's box on
// the rule (the flex content box starts below the border, so a bare -50%
// would sit the rule's width too low). Muted ink keeps it recessive against
// the maroon stamp below — decorative, and 6.00:1 on paper either way.
.stub__tear-mark {
  background: var(--color-surface);
  color: var(--color-stamp-pending);
  font-size: var(--text-body);
  margin-right: var(--spacing-1);
  padding: 0 var(--spacing-1);
  transform: translateY(calc(-50% - var(--border-hairline)));
}

@media (min-width: 768px) {
  .stub__tear {
    margin-inline: calc(-1 * var(--spacing-8));
  }
}

// The stub is one document, not a frame inside a frame: the panel body's
// padding is the single margin, so StepAck's own is handed back. Anchoring on
// .stub adds a level, because StepAck's own `.ack` rule is an equally
// specific single class on its scoped root — at equal weight the winner would
// come down to stylesheet order, which is not a thing to leave to the bundler.
.stub .stub__ack {
  padding: 0;
}

// Restart as a stamp action: square cell ruled in the stamp's own ink,
// tracked small caps — the same cell geometry as every other stamp on the
// page. `color="primary"` emits .text-primary with !important, and the global
// bridge pins outline borders to --color-border-input, so both the label and
// the outer rule are re-ruled here in stamp ink (maroon on paper 10.87:1).
// Anchoring on .stub lifts every selector above the global .q-btn rules.
//
// No .type-eyebrow available: this targets a Quasar-internal through :deep(),
// so there is no authored tag to hang the role class on. The register stays
// spelled out here.
.stub :deep(.ack__restart) {
  border-radius: 0;
  color: var(--color-stamp) !important;
  font-size: var(--text-caption);
  letter-spacing: var(--tracking-eyebrow);
  padding: 0 var(--spacing-6);
  text-transform: uppercase;
}

.stub :deep(.ack__restart::before) {
  border-color: var(--color-stamp);
}

// Second hairline ruled inside the first — the double edge StepAck's stamp
// is struck with. The rules are the elevation; no shadow rides with them.
// Safe on a free pseudo: Quasar's .q-btn uses ::before for its outline and
// sets no ::after, and the button is position: relative to anchor this.
.stub :deep(.ack__restart::after) {
  border: var(--border-hairline) solid currentColor;
  content: "";
  inset: var(--spacing-1);
  pointer-events: none;
  position: absolute;
}

// Press the stamp: the ink darkens on label, outer rule and inner rule
// together (currentColor), never leaving the palette.
.stub :deep(.ack__restart:hover) {
  color: var(--color-secondary-hover) !important;
}

.stub :deep(.ack__restart:hover::before) {
  border-color: var(--color-secondary-hover);
}
</style>
