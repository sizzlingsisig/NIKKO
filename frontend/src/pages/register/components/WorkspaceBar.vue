<script setup lang="ts">
// WorkspaceBar: the register workspace's masthead — a pinned title line
// over the rule-entry hairline; static markup, no props and no emits.
</script>

<template>
  <!-- Masthead: bold body ink sits above a single hairline rule (rule-entry,
       3.48:1), which closes the line the way every control boundary on the
       page does. Deliberately sans and body-sized so the serif headlines
       inside the DocketPanel and briefing cards below keep the display
       voice; balance evens the wrap when the line breaks on mid widths. -->
  <header class="workspace-bar">
    <h2 class="workspace-bar__title"
      >University of the Philippines Visayas - Organization Registration
      Portal</h2
    >
  </header>
</template>

<style scoped lang="scss">
.workspace-bar {
  border-bottom: var(--border-hairline) solid var(--color-rule-entry);
  padding: var(--spacing-3) 0;
}

// Title: body ink — 13.69:1 on paper (documented, app.scss) — bold, with
// the h2 margin zeroed. break-word only rescues a token wider than the
// column; balance keeps a two-line wrap even.
.workspace-bar__title {
  font-size: var(--text-body);
  font-weight: 700;
  line-height: var(--leading-body);
  margin: 0;
  min-width: 0;
  overflow-wrap: break-word;
  text-wrap: balance;
}
</style>
