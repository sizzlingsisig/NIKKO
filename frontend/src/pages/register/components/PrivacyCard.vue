<script setup lang="ts">
// PrivacyCard: the persistent RA 10173 guarantee — pinned copy, no props,
// no slots, nothing swapped per step (spec §6.2). The mockup's maroon left
// rule is what marks it as the card that never changes; Task 5 mounts it
// between the step overview and the guidelines.
</script>

<template>
  <!-- Paper card with the mockup's 2px maroon left accent, hairline edges
       elsewhere, square corners. The lock glyph leads the heading
       (aria-hidden — the heading text carries the meaning), the body copy
       follows, then a hairline rule divides the footer row: label left,
       byte count right. -->
  <section class="privacy-card">
    <h3 class="privacy-card__heading">
      <svg
        class="privacy-card__lock"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
        aria-hidden="true"
        focusable="false"
      >
        <rect x="3" y="11" width="18" height="11" rx="2" />
        <path d="M7 11V7a5 5 0 0 1 10 0v4" />
      </svg>
      <span>RA 10173 PRIVACY GUARANTEE</span>
    </h3>

    <p class="privacy-card__body type-body">
      In compliance with the Philippine Data Privacy Act of 2012, your Form 5
      never leaves this device or transmits to any cloud server. Zero server
      upload residue.
    </p>

    <hr class="privacy-card__rule" />

    <p class="privacy-card__footer">
      <span class="privacy-card__footer-label">STORAGE RESIDUE</span>
      <span class="privacy-card__footer-value">0 BYTES RETAINED</span>
    </p>
  </section>
</template>

<style scoped lang="scss">
// Frame: the shared paper card — hairline edge, square corners, no shadow —
// plus the mockup's maroon left rule. Declared after `border` so the 2px
// accent wins the cascade; this is the one deliberate >1px side accent on
// the page, pinned verbatim by the brief ("per mockup").
.privacy-card {
  background: var(--color-surface);
  border: var(--border-hairline) solid var(--color-rule-hairline);
  border-left: var(--border-rule) solid var(--color-secondary);
  border-radius: 0;
  box-shadow: var(--elevation-rest);
  display: grid;
  gap: var(--spacing-3);
  padding: var(--spacing-6);
}

// Heading: body-scale bold caps, eyebrow-tracked — the clause voice the RA
// string carries (the serif display headline belongs to the step overview
// card above it). Ink on paper (13.69:1); the lock inherits that ink.
//
// No role class: body-SIZE bold with eyebrow tracking, and the ladder has no
// such role — .type-body-strong carries no tracking, .type-eyebrow would drop
// it to caption. The register stays spelled out.
.privacy-card__heading {
  align-items: center;
  color: var(--color-foreground);
  display: flex;
  font-size: var(--text-body);
  font-weight: var(--weight-bold);
  gap: var(--spacing-2);
  letter-spacing: var(--tracking-eyebrow);
  line-height: var(--leading-body);
  margin: 0;
}

// Lock glyph: inline, aria-hidden, currentColor — it takes the heading's
// ink and scales with it (1em), so no pixel size is pinned anywhere.
.privacy-card__lock {
  flex: none;
  height: 1em;
  width: 1em;
}

// Body copy: body size, ink (13.69:1 on this card's paper). Hand-wrapped
// in source; HTML collapses the line breaks to single spaces, so the
// sentence renders exactly as pinned. .type-body matches exactly; this rule
// keeps the ink and margin.
.privacy-card__body {
  color: var(--color-foreground);
  margin: 0;
}

// Hairline rule before the footer — control-boundary ink (rule-entry,
// 3.48:1); border reset plus height:0 leave only the token hairline.
.privacy-card__rule {
  border: 0;
  border-top: var(--border-hairline) solid var(--color-rule-entry);
  height: 0;
  margin: 0;
  width: 100%;
}

// Footer row: label left in muted mono, byte count right in ink — the
// brief's left/right split. flex-wrap lets the value drop onto its own
// line if a narrow rail ever starves the row; margin-left auto pins it
// right whether it shares the row or wraps.
.privacy-card__footer {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-1) var(--spacing-3);
  margin: 0;
}

// Muted machine label — 6.00:1 on paper (documented, app.scss).
.privacy-card__footer-label {
  color: var(--color-foreground-muted);
  font-family: var(--font-mono);
  font-size: var(--text-caption);
  letter-spacing: var(--tracking-eyebrow);
  line-height: var(--leading-caption);
}

// The emphasis pair: ink (13.69:1) against the label's muted (6.00:1) —
// emphasis by contrast alone, since the self-hosted mono ships weight 400
// only (a 700 would just faux-bold).
.privacy-card__footer-value {
  color: var(--color-foreground);
  flex: none;
  font-family: var(--font-mono);
  font-size: var(--text-caption);
  letter-spacing: var(--tracking-eyebrow);
  line-height: var(--leading-caption);
  margin-left: auto;
}

// ≥768px: padding grows with the other cards (DESIGN.md card rhythm).
@media (min-width: 768px) {
  .privacy-card {
    padding: var(--spacing-8);
  }
}
</style>
