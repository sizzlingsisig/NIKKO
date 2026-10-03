<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{ code: string }>();

interface Segment {
  text: string;
  kind: "keyword" | "function" | "plain";
}

const KEYWORDS = new Set([
  "select",
  "from",
  "over",
  "partition",
  "order",
  "by",
  "desc",
  "qualify",
  "row_number",
  "attach",
  "as"
]);

/** Tokenises into segments rather than injecting HTML — no v-html anywhere. */
const segments = computed<Segment[]>(() => {
  const tokens = props.code.split(/(\s+|[();,.*/])/).filter(Boolean);
  return tokens.map(token => {
    const lower = token.toLowerCase();
    if (/^row_number$/i.test(token))
      return { text: token, kind: "function" as const };
    if (KEYWORDS.has(lower)) return { text: token, kind: "keyword" as const };
    return { text: token, kind: "plain" as const };
  });
});
</script>

<template>
  <!-- Ledger entry for the dedupe query: ruled maroon head band, then the
       statement on sunken stock. figure/figcaption because <pre> may only
       contain phrasing content — the caption cannot live inside it. -->
  <figure class="sql-block">
    <figcaption class="sql-block__caption type-eyebrow-mono"> SQL </figcaption>
    <pre class="sql-block__code"><code><span
      v-for="(segment, index) in segments"
      :key="index"
      :class="`sql-block__${segment.kind}`"
    >{{ segment.text }}</span></code></pre>
  </figure>
</template>

<style scoped lang="scss">
// Square-cut ruled frame; elevation declared once (the hairline border).
.sql-block {
  background: var(--color-surface-sunken);
  border: var(--border-hairline) solid var(--color-rule-hairline);
  border-radius: 0;
  box-shadow: var(--elevation-rest);
  margin: var(--spacing-4) 0;
  max-width: 100%;
}

// Ruled caption, same idiom as the slip header: maroon ink on the sunken
// stock, closed by the strong maroon rule the ledger uses. Mono because the
// caption is a field label for the statement beneath it — which is exactly
// what .type-eyebrow-mono is for. (This register was spelled out by hand
// before that role existed.)
.sql-block__caption {
  background: var(--color-surface-sunken);
  border-bottom: var(--border-rule) solid var(--color-secondary);
  color: var(--color-secondary);
  margin: 0;
  padding: var(--spacing-2) var(--spacing-4);
}

// SQL is code/data — mono stack, ledger hairline rules, no costume.
.sql-block__code {
  color: var(--color-foreground); // graphite on stock, AAA
  display: block;
  font-family: var(--font-mono);
  font-size: var(--text-caption);
  line-height: var(--leading-body);
  margin: 0;
  overflow-x: auto;
  padding: var(--spacing-4);
  tab-size: 2;
}

// Keywords maroon, functions pine — both measured AAA on sunken stock
// (maroon ~10.3:1, teal ~9.9:1), and the weight carries the distinction
// for readers who cannot separate the hues.
.sql-block__keyword {
  color: var(--color-secondary);
  font-weight: var(--weight-bold);
}

.sql-block__function {
  color: var(--color-primary);
  font-weight: var(--weight-bold);
}
</style>
