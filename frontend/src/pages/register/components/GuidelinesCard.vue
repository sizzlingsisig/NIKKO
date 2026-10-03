<script setup lang="ts">
// GuidelinesCard: the sidebar's per-step checklist. The copy is pinned per
// variant (spec §6.3, mockup), so the card keys everything off one token —
// Task 7 passes variant = ["upload", "review", "next"][step] and the
// heading plus three entries swap themselves. Single-root <section>: the
// caller's id and tabindex="-1" fallthrough land on the card, which is what
// lets the panel's "GUIDELINES & FAQ" button focus it (Task 7).

/** Which step's checklist the card is showing. */
type Variant = "upload" | "review" | "next";

/** One entry: filing label (carrying its own 01/02/03 number) + body. */
interface Entry {
  label: string;
  body: string;
}

/** Heading per variant — verbatim, § clause mark included. */
const HEADINGS: Record<Variant, string> = {
  upload: "§ DOCUMENT GUIDELINES",
  review: "§ REVIEW GUIDELINES",
  next: "§ WHAT HAPPENS NEXT"
};

/** Three entries per variant, in order. Pinned copy — do not reword. */
const ITEMS: Record<Variant, readonly Entry[]> = {
  upload: [
    {
      label: "01 / GENUINE DOCUMENT",
      body: "Form 5 PDF downloaded directly from university SAIS or CRS student portals."
    },
    {
      label: "02 / UNMODIFIED INTEGRITY",
      body: "Files with modified text, altered timestamps, or missing watermarks will fail checksum."
    },
    {
      label: "03 / IN-PERSON REGISTRAR",
      body: "If automated parsing fails, visit the Office of the University Registrar counters."
    }
  ],
  review: [
    {
      label: "01 / CHECK YOUR ENTRIES",
      body: "Confirm student number, name, degree program, college and year level against your Form 5."
    },
    {
      label: "02 / ATTACH REQUIRED FILES",
      body: "Upload your 2×2 photo and white-paper signature scan (JPG/PNG)."
    },
    {
      label: "03 / CONSENT TO PROCEED",
      body: "Tick the RA 10173 consent box; submission requires your agreement."
    }
  ],
  next: [
    {
      label: "01 / ONE REFERENCE ID",
      body: "Your REG-YYYY-NNNNN ID is the proof of this submission — keep it."
    },
    {
      label: "02 / ADMIN DEDUPE",
      body: "Org admins keep the latest submission per student."
    },
    {
      label: "03 / ROSTER EXPORT",
      body: "The deduplicated roster is exported as CSV/XLSX."
    }
  ]
};

defineProps<{
  variant: Variant;
}>();
</script>

<template>
  <!-- Paper card in the same frame as its siblings; single root so the
       caller's focus attributes fall through. The <ol> keeps list semantics
       with its markers stripped — each label carries its own 01/02/03
       number — so role="list" holds what Safari drops for markerless lists
       (PhaseStrip's pattern). Entries divide on hairlines. -->
  <section class="guidelines-card">
    <h3 class="guidelines-card__heading">{{ HEADINGS[variant] }}</h3>

    <ol class="guidelines-card__list" role="list">
      <li
        v-for="entry in ITEMS[variant]"
        :key="entry.label"
        class="guidelines-card__item"
      >
        <p class="guidelines-card__label">{{ entry.label }}</p>
        <p class="guidelines-card__copy type-body">{{ entry.body }}</p>
      </li>
    </ol>
  </section>
</template>

<style scoped lang="scss">
// Frame: the shared sidebar card — paper ground, hairline edge, square
// corners, no shadow — on the same block rhythm as its siblings.
.guidelines-card {
  background: var(--color-surface);
  border: var(--border-hairline) solid var(--color-rule-hairline);
  border-radius: 0;
  box-shadow: none;
  display: grid;
  gap: var(--spacing-3);
  padding: var(--spacing-6);
}

// Heading: the clause voice the privacy card uses — body-scale bold caps,
// eyebrow-tracked, ink on paper (13.69:1). The § ships inside the pinned
// copy, so no transform rides along (the string is caps already).
//
// No role class: this is body-SIZE bold with eyebrow tracking, and the ladder
// has no such role — .type-body-strong carries no tracking, .type-eyebrow
// would drop it to caption. The register stays spelled out.
.guidelines-card__heading {
  color: var(--color-foreground);
  font-size: var(--text-body);
  font-weight: var(--weight-bold);
  letter-spacing: var(--tracking-eyebrow);
  line-height: var(--leading-body);
  margin: 0;
}

// The list: markers stripped, stacked on the 12px rhythm.
.guidelines-card__list {
  display: grid;
  gap: var(--spacing-3);
  list-style: none;
  margin: 0;
  padding: 0;
}

// Entries divide on hairlines: gap above the rule, padding below it, so
// the divider sits midway between two entries (rule-entry, 3.48:1).
.guidelines-card__item + .guidelines-card__item {
  border-top: var(--border-hairline) solid var(--color-rule-entry);
  padding-top: var(--spacing-3);
}

// Filing label: mono maroon caps, eyebrow-tracked — maroon on this card's
// paper is 10.87:1 (documented, app.scss). Weight stays 400: the
// self-hosted mono ships one weight only, so 700 would just faux-bold.
.guidelines-card__label {
  color: var(--color-secondary);
  font-family: var(--font-mono);
  font-size: var(--text-caption);
  letter-spacing: var(--tracking-eyebrow);
  line-height: var(--leading-caption);
  margin: 0 0 var(--spacing-1);
}

// Entry copy: body size, ink (13.69:1 on paper). Margin zeroed because it
// is a <p>. .type-body matches exactly; this rule keeps the ink and margin.
.guidelines-card__copy {
  color: var(--color-foreground);
  margin: 0;
}

// ≥768px: padding grows with the other cards (DESIGN.md card rhythm).
@media (min-width: 768px) {
  .guidelines-card {
    padding: var(--spacing-8);
  }
}
</style>
