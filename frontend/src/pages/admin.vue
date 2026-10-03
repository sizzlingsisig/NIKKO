<script setup lang="ts">
import { useQuasar } from "quasar";

import AdminTokenGate from "@/components/AdminTokenGate.vue";
import AppCard from "@/components/AppCard.vue";
import AppChip from "@/components/AppChip.vue";
import RosterTable from "@/components/RosterTable.vue";
import SqlBlock from "@/components/SqlBlock.vue";
import StatTile from "@/components/StatTile.vue";
import { buildRosterCsv, CSV_FILENAME } from "@/domain/roster";
import { useAdminStore } from "@/stores/admin";
import { useRosterStore } from "@/stores/roster";

const DEDUPE_SQL = `ATTACH 'registrations.db' AS rosters (sqlite);
SELECT * FROM rosters.registrations
QUALIFY ROW_NUMBER() OVER (PARTITION BY student_number ORDER BY submitted_at DESC) = 1;`;

const $q = useQuasar();
const admin = useAdminStore();
const roster = useRosterStore();

function onSignIn(token: string) {
  if (admin.signIn(token)) {
    $q.notify({
      message: "Token accepted (simulated auth, FR-4.1).",
      color: "dark",
      position: "bottom",
      timeout: 3400
    });
  }
}

function onExportCsv() {
  const blob = new Blob([buildRosterCsv(roster.rows)], {
    type: "text/csv;charset=utf-8"
  });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = CSV_FILENAME;
  anchor.click();
  // Release the object URL once the download has been handed to the browser.
  setTimeout(() => URL.revokeObjectURL(url), 4000);
  $q.notify({
    message: `CSV exported. Latest record per student (${roster.stats.unique} rows).`,
    color: "dark",
    position: "bottom",
    timeout: 3400
  });
}

function onExportXlsx() {
  $q.notify({
    message:
      "Simulated: in production DuckDB COPY … FORMAT XLSX streams the same deduplicated result.",
    color: "dark",
    position: "bottom",
    timeout: 4200
  });
}
</script>

<template>
  <div class="console">
    <AdminTokenGate v-if="!admin.isAuthenticated" @submit="onSignIn" />

    <!-- The counterfoil book. One slip (AppCard) carries the ruled head and
         the metadata strip below it; the body files every section on a
         ruled margin: the ledger summary, the query entry, the export stamps,
         the legend, and the ledger itself. The sections draw no frames of their
         own: StatTile, SqlBlock and RosterTable keep theirs, and the page is
         not a grid of cards with a hero metric on top. -->
    <template v-else>
      <AppCard title="Membership Roster: Export Console">
        <template #actions>
          <!-- Session control on the header's metadata strip. Its stamp
               geometry lives in the styles below, so it matches the book's
               other cells instead of arriving as Quasar's teal pill. -->
          <q-btn
            class="console__stamp"
            outline
            color="primary"
            label="Sign out"
            @click="admin.signOut()"
          />
        </template>

        <!-- The book's margin: one maroon rule, and every section filed off
             it. The header above and the paper around it stay AppCard's. -->
        <div class="console__margin">
          <!-- The ledger's summary: raw, unique and collapsed filed as three
               ruled columns on one continuous stock band, their counts set in
               mono with tabular figures so they align down the page. -->
          <div class="console__summary">
            <StatTile :value="roster.stats.raw" label="Raw submissions" />
            <StatTile :value="roster.stats.unique" label="Unique students" />
            <StatTile
              :value="roster.stats.collapsed"
              label="Duplicate rows collapsed"
            />
          </div>

          <!-- The dedupe rule, filed as a ledger entry: SqlBlock's maroon
               caption band heads the statement, which is data, so it prints in
               mono. -->
          <div class="console__section console__query">
            <SqlBlock :code="DEDUPE_SQL" />
          </div>

          <!-- Export stamps, with the policy stamp that governs both. -->
          <div class="console__section console__exports">
            <div class="console__export-row">
              <q-btn
                class="console__export"
                unelevated
                color="primary"
                icon="download"
                label="Export deduplicated CSV"
                @click="onExportCsv"
              />
              <q-btn
                class="console__stamp"
                outline
                color="primary"
                icon="download"
                label="Export .xlsx"
                @click="onExportXlsx"
              />
            </div>
            <AppChip label="DEDUP: LATEST PER STUDENT" tone="positive" />
          </div>

          <!-- The legend, then the ledger it explains. The key class names are
               the row classes RosterTable stamps, so the sentence and the
               table agree in code as well as in ink. -->
          <div class="console__section console__ledger">
            <p class="console__legend type-body">
              Rows highlighted <strong class="is-latest">green</strong> are the
              versions exported (latest <code>submitted_at</code> per student);
              <strong class="is-collapsed">red</strong> rows are earlier
              re-submissions collapsed by the window function (FR-4.3).
              Registrations you submit in the Register tab appear here in real
              time.
            </p>

            <RosterTable :rows="roster.annotated" />
          </div>
        </div>
      </AppCard>
    </template>
  </div>
</template>

<style scoped lang="scss">
// ============================================================================
// The counterfoil book
// ----------------------------------------------------------------------------
// The page owns the sheet its components sit on — the binding margin rule, the
// seams between sections, the stamp cells, the browser surfaces — and nothing
// else. The band, the tiles, the SQL entry, the chip and the ledger all keep
// the frames they brought with them.
//
// `.console` anchors the page-level rule below, and each section anchors its
// own deeper rule. Anchoring there lifts a selector a level above the Quasar
// bridge (app.scss) and above a component's own root rule (one scoped class,
// two selectors of weight), where the winner would otherwise come down to
// stylesheet order.
// ============================================================================

// The book's binding margin: one 1px maroon rule with a ledger's inset, hung
// with every section. 1px is the ceiling the craft-floor sets for a coloured
// side border — above that it reads as a callout, not as a rule. A ledger's
// margin is asymmetric by nature, so the entries sit right of it; that is the
// bind.
.console__margin {
  border-left: var(--border-hairline) solid var(--color-rule-strong);
  padding-left: var(--spacing-3);
}

// The seam: the strong maroon rule that files each section, with more air above
// the rule than between it and what the section holds. The first section (the
// summary) sits directly under the header's closing rule and takes no seam.
.console__section {
  border-top: var(--border-rule) solid var(--color-rule-strong);
  margin-top: var(--spacing-6);
  padding-top: var(--spacing-4);
}

// ---- Ledger summary strip ---------------------------------------------------
// Three cells filed side by side on one stock band. StatTile brings its own
// frame, column head and mono value; the strip hands the interior edges back so
// the row reads as one ruled band instead of three cards in a slip.
.console__summary {
  display: grid;
  gap: 0;
  grid-template-columns: minmax(0, 1fr);
}

// Stacked: each cell climbs onto the one above it, so the two hairlines share a
// single rule instead of doubling into a seam. Anchoring on the strip puts this
// at four selectors of weight, above StatTile's own root rule at two, so the
// win never depends on which stylesheet the bundler emits first.
.console__summary :deep(.stat-tile + .stat-tile) {
  margin-top: calc(-1 * var(--border-hairline));
}

// ---- Query entry ------------------------------------------------------------
// SqlBlock brings its own frame and caption band; the section owns the space
// around it, so its own vertical margins are handed back rather than stacked on
// the seam. Anchoring on .console__query lifts this above that root rule.
.console__query :deep(.sql-block) {
  margin: 0;
}

// ---- Export stamps ----------------------------------------------------------
// The policy stamp and the actions share the ruled line, the stamp cell
// centred on it.
.console__exports {
  align-items: center;
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-3) var(--spacing-6);
  justify-content: space-between;
}

.console__export-row {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-3);
}

// Shared stamp geometry: square-cut cells with tracked small caps, the cell
// this book presses everything with. Global .q-btn already carries the 44px
// floor; restated so the target survives a bridge change.
//
// No .type-eyebrow here, deliberately — same reason as MainLayout's
// .letterhead__link: these are <q-btn>s, and app.scss's global .q-btn lands
// after .type-eyebrow at equal specificity (0-1-0), so the role class would
// lose and the register has to stay spelled out in this 0-2-0 scoped rule.
.console__stamp,
.console__export {
  border-radius: 0;
  font-size: var(--text-caption);
  letter-spacing: var(--tracking-eyebrow);
  min-height: var(--touch-target);
  text-transform: uppercase;
}

// The ruled stamp: ink label in tracked small caps. `color="primary"` emits
// .text-primary with !important, so the label is re-stated in ink (12:1 on
// paper) — a cell that reads as the book's own mark rather than as a second
// teal call to action. The icon rides currentColor with the label, so both
// clear AA together rather than the label carrying it alone.
.console__stamp {
  color: var(--color-foreground) !important; // ink on paper ~12:1
}

// The rule is named here rather than inherited: --color-rule-entry is the
// control boundary (3.48:1), the same token the global bridge pins, so the
// decision stays legible on the page that owns the cell.
.console__stamp::before {
  border-color: var(--color-rule-entry);
}

.console__stamp:hover::before {
  border-color: var(--color-foreground);
}

// The warm fill needs !important because .q-btn--outline pins a transparent
// background; :not(.disabled) keeps a dead control from implying it is live.
.console__stamp:not(.disabled):hover {
  background: var(--color-surface-sunken) !important;
}

// The filing stamp: Quasar's teal cell in the book's square cut, still white on
// it at 10.33:1. `color="primary"` emits .bg-primary with !important, so the
// hover fill is re-stated here — the cell deepens into the brand's own hover
// instead of washing off-world.
.console__export:not(.disabled):hover {
  background: var(--color-primary-hover) !important;
}

// Claimed: the amber hairline rides the cell's own edge — 5.96:1 against the
// filled teal cell, and hard against ink on a ruled cell, which inks its frame
// first so the ring never carries the state alone (amber on paper is 1.73:1).
// Only the ruled cell inks a frame: Quasar draws no ::before border on an
// unelevated button, and there the fill is what sits under the ring. Declared
// after the hover rules so a focused cell that is also hovered still reads as
// claimed. Both outrank the global :focus-visible ring.
.console__stamp:focus-visible::before {
  border-color: var(--color-foreground);
}

.console__stamp:focus-visible,
.console__export:focus-visible {
  outline: var(--border-rule) solid var(--color-rule-focus);
  outline-offset: 0;
}

// ---- Legend ----------------------------------------------------------------
// Fine print on the ledger page: muted ink at the body size, held to a readable
// measure (6.00:1 on paper) beside a table three times as wide.
// .type-body carries the register; this rule keeps colour, measure and rhythm.
.console__legend {
  color: var(--color-foreground-muted);
  margin: 0 0 var(--spacing-6);
  max-width: 68ch; // 60-80 character measure
}

// `submitted_at` is a column name, so it is data and takes the mono stack. The
// global bridge already hands `code` that family; it is restated here so the
// note's one code span cannot fall back to the sans if the bridge ever moves.
.console__legend code {
  color: var(--color-foreground);
  font-family: var(--font-mono);
  font-size: var(--text-body);
}

// The keys name the row tints RosterTable paints, so each wears the swatch it
// describes: the row's own tint, ruled in the ink its word already wears. The
// rules are those inks (green 5.05:1, maroon 10.87:1 on paper), so the keys
// clear 3:1 as non-text boundaries. The square is 0.75em — 12px at the body
// size — dropped 0.1em to sit on the line instead of floating to the cap
// height, the way a printed key does.
.console__legend .is-latest::before,
.console__legend .is-collapsed::before {
  border: var(--border-hairline) solid currentColor;
  content: "";
  display: inline-block;
  height: 0.75em;
  margin-right: var(--spacing-1);
  vertical-align: -0.1em;
  width: 0.75em;
}

.console__legend .is-latest::before {
  background: var(--color-success-soft);
}

.console__legend .is-collapsed::before {
  background: var(--color-secondary-soft);
}

// ---- Browser surfaces ------------------------------------------------------
// Selection anywhere in the book takes the amber claim tint (graphite on it
// stays ≥4.5:1) — the same selection the register surfaces print in.
.console ::selection {
  background: var(--color-accent-soft);
  color: var(--color-foreground);
}

// The ledger scrolls sideways on a phone, and the one scrollbar this page draws
// for itself comes from the palette: thumb on sunken stock, ~3.1:1 between
// them. `scrollbar-color` is the standard pair; no vendor track art.
.console__ledger :deep(.roster-table) {
  scrollbar-color: var(--color-border-input) var(--color-surface-sunken);
}

@media (min-width: 640px) {
  // Side by side: the first cell's right rule is the column rule, so the rest
  // hand theirs back and the strip becomes one band of three columns.
  .console__summary {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }

  .console__summary :deep(.stat-tile + .stat-tile) {
    border-left: 0;
    margin-top: 0;
  }
}

@media (min-width: 768px) {
  .console__margin {
    padding-left: var(--spacing-4);
  }
}
</style>
