<script setup lang="ts">
import { computed } from "vue";

import type { AnnotatedRosterRow } from "@/domain/registration";

const props = defineProps<{ rows: readonly AnnotatedRosterRow[] }>();

const COLUMNS = [
  { name: "id", label: "ID", field: "id", align: "left" as const },
  {
    name: "student_number",
    label: "Student No.",
    field: "student_number",
    align: "left" as const,
    classes: "is-mono"
  },
  {
    name: "full_name",
    label: "Full Name",
    field: "full_name",
    align: "left" as const
  },
  {
    name: "degree_program",
    label: "Degree Program",
    field: "degree_program",
    align: "left" as const
  },
  {
    name: "college",
    label: "College",
    field: "college",
    align: "left" as const
  },
  {
    name: "year_level",
    label: "Yr",
    field: "year_level",
    align: "left" as const
  },
  {
    name: "up_mail",
    label: "UP Mail",
    field: "up_mail",
    align: "left" as const,
    classes: "is-mono"
  },
  {
    name: "submitted_at",
    label: "Submitted (UTC)",
    field: "submitted_at",
    align: "left" as const,
    classes: "is-mono"
  },
  {
    name: "ref",
    label: "Ref",
    field: "ref",
    align: "left" as const,
    classes: "is-mono"
  }
];

/** Winning row is exported (green); superseded rows are collapsed (amber). */
function rowClass(row: AnnotatedRosterRow): string {
  return row.is_latest ? "is-latest" : "is-collapsed";
}

const tableRows = computed(() => props.rows);
</script>

<template>
  <!-- Counterfoil ledger: ruled rows on ruled stock, earlier copies struck
       through so the collapse is shown, not hidden (PRODUCT dedupe
       transparency). Row semantics and slot contracts are untouched. -->
  <q-table
    flat
    bordered
    separator="horizontal"
    row-key="id"
    :rows="tableRows"
    :columns="COLUMNS"
    :row-class="rowClass"
    no-data-label="No submissions yet."
    class="roster-table"
    :aria-label="'Membership roster, newest submission per student highlighted'"
  >
    <!-- QTable renders its `top` slot outside the <table>, so a <caption>
         would be invalid here; this is the screen-reader equivalent. -->
    <template #top>
      <span class="sr-only">
        Membership roster, newest submission per student highlighted
      </span>
    </template>

    <template #body-cell-ref="slotProps">
      <q-td :props="slotProps">
        {{ slotProps.row.ref }}
        <q-badge
          :color="slotProps.row.is_latest ? 'positive' : 'secondary'"
          :label="slotProps.row.is_latest ? 'exported' : 'collapsed'"
          class="roster-table__badge"
        />
      </q-td>
    </template>
  </q-table>
</template>

<style scoped lang="scss">
// Ledger page: square-cut frame, elevation declared once (hairline border).
.roster-table {
  background: var(--color-surface);
  border: var(--border-hairline) solid var(--color-rule-hairline);
  border-radius: 0;
  box-shadow: var(--elevation-rest);
  font-size: var(--text-body);
  overflow-x: auto;
}

.roster-table :deep(table) {
  min-width: 60rem;
}

// Column heads: tracked small caps (global Quasar bridge) over sunken stock,
// closed by the maroon ruled line that heads every ledger page. The border
// color override also recolours Quasar's separator, which otherwise paints
// in currentColor (ink) at full weight.
.roster-table :deep(th) {
  border-bottom-color: var(--color-rule-strong);
  color: var(--color-foreground-muted); // on sunken 5.30:1
  padding: var(--spacing-3) var(--spacing-4);
  white-space: nowrap;
}

// Ruled rows: Quasar draws horizontal separators as border-bottom; repaint
// them hairline so the rules read as stationery, not as table chrome.
// Row height lands on the 48px rhythm the header and empty page follow.
.roster-table :deep(td) {
  border-bottom-color: var(--color-rule-hairline);
  font-size: var(--text-body);
  padding: var(--spacing-3) var(--spacing-4);
  white-space: nowrap;
}

// Plain rows only — rows carrying a dedupe verdict keep their tint.
.roster-table :deep(tbody tr:not(.is-latest):not(.is-collapsed):hover td) {
  background: var(--color-surface-sunken);
}

// Winning row — exported. Green tint is contract with the legend copy.
.roster-table :deep(tr.is-latest td) {
  background: var(--color-success-soft);
}

// Superseded row — the earlier copy, struck through in maroon against its
// wine tint (strike on tint 9.51:1). The strike stops before the ref cell:
// the verdict stamp (ref + "collapsed" badge) stays clean, so the row reads
// "these fields are dead, here is why". Wine (not amber) so the row tint,
// the "collapsed" badge and the legend copy all agree.
.roster-table :deep(tr.is-collapsed td) {
  background: var(--color-secondary-soft);
}

.roster-table :deep(tr.is-collapsed td:not(:last-child)) {
  text-decoration-color: var(--color-secondary);
  text-decoration-line: line-through;
  text-decoration-thickness: 1px;
}

// Mono columns (IDs, mails, timestamps, refs) — tabular figures so the
// ledger's numbers align. :deep because QTable renders these cells itself,
// outside this component's scope.
.roster-table :deep(td.is-mono) {
  font-family: var(--font-mono);
  font-size: var(--text-body);
  font-variant-numeric: tabular-nums;
}

// Rubber-stamp verdict: tracked small caps, square-cut.
//
// No .type-eyebrow here: this is a <q-badge>, and Quasar pins the badge's own
// line-height as part of its vertical box — restating it would resize the
// stamp, not just relabel it. The scoped rule is already 0-2-0 and outranks
// both Quasar's .q-badge and a 0-1-0 role class, so the register stays here.
.roster-table__badge {
  border-radius: 0;
  font-size: var(--text-caption);
  font-weight: var(--weight-bold);
  letter-spacing: var(--tracking-eyebrow);
  margin-left: var(--spacing-2);
  padding: 2px var(--spacing-2);
  text-transform: uppercase;
}

// Empty ledger page: sunken stock ruled to the same 48px row rhythm the
// table uses, so the page reads as waiting for its first entry rather than
// as an error state. Message colour is muted-on-stock (5.30:1).
//
// No role class is available to this rule at all: it targets a Quasar-internal
// element reached through :deep(), so there is no authored tag in this
// template to hang .type-eyebrow on. The register is spelled out here.
.roster-table :deep(.q-table__bottom--nodata) {
  align-items: center;
  background-color: var(--color-surface-sunken);
  background-image: repeating-linear-gradient(
    to bottom,
    transparent 0 47px,
    var(--color-rule-hairline) 47px 48px
  );
  border-top: var(--border-hairline) solid var(--color-rule-hairline);
  color: var(--color-foreground-muted);
  display: flex;
  font-size: var(--text-caption);
  font-weight: var(--weight-bold);
  letter-spacing: var(--tracking-eyebrow);
  min-height: 12rem;
  padding: var(--spacing-4) var(--spacing-6);
  text-transform: uppercase;
}

.roster-table :deep(.q-table__bottom-nodata-icon) {
  color: var(--color-foreground-muted);
  // Doubles the caption-sized .q-table__bottom--nodata below (12px -> 24px),
  // which is exactly what Quasar's own `font-size: 200%` resolved to. Anchored
  // on --text-caption, not --text-body: the old value was 24px and 24px is on
  // the scale, while 2x body would be an off-scale 32px.
  font-size: calc(var(--text-caption) * 2);
  margin-right: var(--spacing-3);
}
</style>
