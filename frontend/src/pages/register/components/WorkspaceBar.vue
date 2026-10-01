<script setup lang="ts">
// WorkspaceBar: the document workspace's header line — static markup, no
// props and no emits. The chip, the docket title and the security meta are
// pinned copy; Task 5 mounts this above the PhaseStrip.
</script>

<template>
  <!-- Header line: the bordered mono chip and the docket title run left, the
       security/compliance meta right, and a hairline rule-entry rule closes
       the line. Below 640px the meta flex-wraps onto its own line beneath
       the title; the title is the only thing allowed to shrink. -->
  <header class="workspace-bar">
    <div class="workspace-bar__id">
      <span class="workspace-bar__chip">DOCUMENT WORKSPACE</span>
      <h2 class="workspace-bar__title"
        >Official University Enrollment Ingestion Docket</h2
      >
    </div>
    <span class="workspace-bar__meta"
      >SECURITY: RESTRICTED · COMPLIANCE: RA 10173</span
    >
  </header>
</template>

<style scoped lang="scss">
// Masthead line: a baseline-aligned flex row closed by the same hairline
// that marks every control boundary (rule-entry, 3.48:1). Compact is the
// base — the <640px case where the meta wraps — and ≥640px joins the row.
.workspace-bar {
  align-items: baseline;
  border-bottom: var(--border-hairline) solid var(--color-rule-entry);
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-2) var(--spacing-3);
  padding: var(--spacing-3) 0;
}

// Left group: chip and title flow as one unit that wraps internally, so on
// a very narrow screen the title can drop under the chip without the chip
// ever being crushed (it refuses to shrink).
.workspace-bar__id {
  display: flex;
  flex: 1 1 auto;
  flex-wrap: wrap;
  gap: var(--spacing-2);
  min-width: 0;
}

// The chip: bordered mono span in maroon rule and maroon ink — 10.87:1 on
// paper (documented, app.scss stamp tokens), 10.1:1 on the canvas this bar
// rests on; both clear AA. Tracked like every eyebrow on the page; the copy
// is already caps, so no transform rides along.
.workspace-bar__chip {
  border: var(--border-hairline) solid var(--color-secondary);
  color: var(--color-secondary);
  flex: none;
  font-family: var(--font-mono);
  font-size: var(--text-caption);
  letter-spacing: var(--tracking-eyebrow);
  line-height: var(--leading-caption);
  padding: var(--spacing-1) var(--spacing-2);
}

// The docket title: bold body ink — 13.69:1 on paper (documented),
// 12.8:1 on the canvas this bar rests on. Deliberately sans and body-sized
// so the serif headline inside the DocketPanel below keeps the display
// voice. Margin zeroed because it is an <h2>.
.workspace-bar__title {
  font-size: var(--text-body);
  font-weight: 700;
  line-height: var(--leading-body);
  margin: 0;
  min-width: 0;
  overflow-wrap: break-word; // narrowest phones may break a long word
}

// Right meta: mono, muted — 6.00:1 on paper, 5.59:1 on the canvas this
// line rests on; both clear AA 4.5:1. flex-basis 100% parks it on its own
// line under the title while the bar is wrapping (<640px).
.workspace-bar__meta {
  color: var(--color-foreground-muted);
  flex: 0 0 100%;
  font-family: var(--font-mono);
  font-size: var(--text-caption);
  letter-spacing: var(--tracking-eyebrow);
  line-height: var(--leading-caption);
}

// ≥640px: the meta joins the row and pins to the right edge; the line
// breathes a little more, the same growth AppCard's band makes.
@media (min-width: 640px) {
  .workspace-bar {
    padding: var(--spacing-4) 0;
  }

  .workspace-bar__meta {
    flex-basis: auto;
    margin-left: auto;
    text-align: right;
  }
}
</style>
