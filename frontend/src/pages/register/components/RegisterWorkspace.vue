<script setup lang="ts">
// RegisterWorkspace: the register page's layout shell. It stacks the
// static WorkspaceBar masthead over the stateful PhaseStrip, then opens
// the two column row the sidebar cards (Privacy/Guidelines) and the
// DocketPanel fill — both arriving as slots, so this component owns no
// content and no layout decisions beyond the grid itself. The wizard
// state rides three props straight through to the PhaseStrip; its jump is
// re-emitted under the same name so the page binds one handler to the
// whole shell.
import WorkspaceBar from "./WorkspaceBar.vue";
import PhaseStrip from "./PhaseStrip.vue";

const props = defineProps<{
  step: number;
  maxReached: number;
  finished: boolean;
}>();

const emit = defineEmits<{ jump: [step: number] }>();
</script>

<template>
  <!-- One grid, four items: the bar and strip ride the full width (each
       spans both columns once the row splits), then the sidebar column and
       the panel. DOM order is sidebar → panel so the desktop grid places
       the sidebar left (30%) and the panel right (1fr); below 900px the
       grid collapses to one column and the order property flips the two —
       panel first, sidebar after — without duplicating a single node. -->
  <div class="workspace">
    <WorkspaceBar />
    <PhaseStrip v-bind="props" @jump="emit('jump', $event)" />
    <aside class="workspace__sidebar">
      <slot name="sidebar" />
    </aside>
    <section class="workspace__panel">
      <slot name="panel" />
    </section>
  </div>
</template>

<style scoped lang="scss">
// The shell: single column by default (the <900px case) with a compact
// vertical rhythm — bar, strip, panel, sidebar. min-width 0 keeps the grid
// track from being forced wider than the viewport by a long unbreakable
// string inside either column.
.workspace {
  display: grid;
  gap: var(--spacing-4);
  grid-template-columns: minmax(0, 1fr);
  min-width: 0;
}

// Compact order: the panel leads, the sidebar trails. Both sit after the
// bar and strip (whose default order is 0) so the header stack stays put;
// the sidebar's DOM position — ahead of the panel, for the desktop columns
// below — never shows on a narrow screen. min-width 0 on both columns, so
// neither is sized past its track by its own content. Both columns are
// flex stacks so their content can fill the grid row the columns share —
// the grid already stretches the two boxes to one height, and these rules
// push that height down to the visible paper inside each column.
.workspace__sidebar {
  display: flex;
  flex-direction: column;
  min-width: 0;
  order: 2;
}

// The last sidebar card absorbs the column's slack, so the card stack
// always reaches the column's bottom edge (a card with spare height keeps
// its content at the top; only its paper extends). No gap: the cards keep
// their existing flush block stacking.
.workspace__sidebar > :last-child {
  flex: 1 0 auto;
}

.workspace__panel {
  display: flex;
  flex-direction: column;
  min-width: 0;
  order: 1;
}

// The docket panel fills its column the same way; DocketPanel's own flex
// column keeps the header at the top and the actions footer on the bottom
// edge as the panel grows.
.workspace__panel > .docket-panel {
  flex: 1 0 auto;
}

// ≥900px: the row splits — sidebar 30%, panel the rest — at the workspace
// rhythm every band on the page grows to. The bar and the strip each span
// both columns so they keep their full width over the split; both are
// children of this component, and Vue puts this component's scope id on a
// child component's root node, so the plain selector reaches them. The two
// columns drop their order override (back to 0 = DOM order), restoring
// sidebar left, panel right.
@media (min-width: 900px) {
  .workspace {
    gap: var(--spacing-6);
    grid-template-columns: minmax(0, 30%) minmax(0, 1fr);
  }

  .workspace > .workspace-bar,
  .workspace > .phase-strip {
    grid-column: 1 / -1;
  }

  .workspace__sidebar,
  .workspace__panel {
    order: 0;
  }
}
</style>
