<script setup lang="ts">
import { nextTick, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";

import AppCrest from "@/components/AppCrest.vue";

const route = useRoute();

const NAV_ITEMS = [
  { label: "Register", to: "/register" },
  { label: "Admin", to: "/admin" }
] as const;

// The active route claims its segment of the foot rule: the 2px rule
// thickens beneath the current link, gilded along its bottom edge.
const claim = ref<HTMLElement | null>(null);
const claimStyle = ref({ width: "0px", transform: "translateX(0px)" });
const claimLive = ref(false);

let claimPlaced = false; // first placement must snap, never slide
let fontsSettled = false;
let fontPoll: number | undefined; // short metric-settling poll, cleared on unmount

function armClaim(): void {
  if (!claimPlaced || !fontsSettled || claimLive.value) return;
  window.requestAnimationFrame(() => {
    // Recalc now: record the final geometry as this element's computed
    // style while no transition exists, so arming .is-live starts nothing.
    // Without this, class-add and style-write land in the same style
    // recalc and the claim slides in from translateX(0) on every load.
    claim.value?.getBoundingClientRect();
    claimLive.value = true;
  });
}

function positionClaim(): void {
  const el = claim.value;
  if (!el) return;
  const rule = el.parentElement;
  const active = document.querySelector<HTMLElement>(
    ".letterhead__link.is-active"
  );
  if (!rule || !active) return; // nav not rendered/matched yet
  const ruleBox = rule.getBoundingClientRect();
  const linkBox = active.getBoundingClientRect();
  claimStyle.value = {
    width: `${linkBox.width}px`,
    transform: `translateX(${linkBox.left - ruleBox.left}px)`
  };
  claimPlaced = true;
  armClaim();
}

watch(
  () => route.path,
  async () => {
    await nextTick();
    positionClaim();
  }
);

onMounted(() => {
  window.addEventListener("resize", positionClaim);
  document.fonts?.addEventListener?.("loadingdone", positionClaim);
  // Place immediately against whatever metrics are live at first paint, so the
  // bar is never absent while the page settles — `positionClaim` re-runs on
  // `loadingdone` and swaps the width/translate for the real ones.
  positionClaim();
  // Fonts can also change metrics with no event at all (a face that resolves
  // from cache mid-paint, or `fonts.ready` having already settled), so poll for
  // a short window rather than trusting the event pair alone. This is a cheap
  // read of two rects and stops the claim from ever landing against stale
  // fallback metrics.
  let settled = false;
  const confirmSettled = (): void => {
    if (settled) return;
    settled = true;
    window.clearInterval(poll);
    window.clearTimeout(poll);
    fontsSettled = true;
    positionClaim();
  };
  const poll = window.setInterval(() => {
    if (document.fonts?.status === "loaded") confirmSettled();
  }, 120);
  fontPoll = poll;
  window.setTimeout(confirmSettled, 1000);
  void document.fonts?.ready.then(confirmSettled);
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", positionClaim);
  document.fonts?.removeEventListener?.("loadingdone", positionClaim);
  if (fontPoll !== undefined) window.clearInterval(fontPoll);
});
</script>

<template>
  <q-layout view="hHh Lpr lFf">
    <q-header class="app-header">
      <div class="letterhead">
        <div class="letterhead__band">
          <div class="letterhead__identity">
            <AppCrest :size="40" class="letterhead__seal" />
            <div class="letterhead__titles">
              <h1 class="letterhead__name">NIKKO</h1>
              <p class="letterhead__window">
                Nexus for Identity-verification, Key-signatures, and Kompiled
                Organization-lists
              </p>
            </div>
          </div>

          <nav class="letterhead__nav" aria-label="Primary">
            <q-btn
              v-for="item in NAV_ITEMS"
              :key="item.to"
              :to="item.to"
              :label="item.label"
              no-caps
              flat
              unelevated
              class="letterhead__link"
              :class="{ 'is-active': route.path === item.to }"
            />
          </nav>
        </div>

        <div class="letterhead__rule">
          <span
            ref="claim"
            class="letterhead__claim"
            :class="{ 'is-live': claimLive }"
            :style="claimStyle"
            aria-hidden="true"
          />
        </div>
      </div>
    </q-header>

    <q-page-container>
      <main class="app-main">
        <slot />
      </main>
    </q-page-container>

    <footer class="app-footer">
      <div class="app-footer__identity">
        <p class="app-footer__org">
          <span class="app-footer__mark" aria-hidden="true" />
          University of the Philippines · Office of Student Affairs &amp;
          Institutional Registrars
        </p>
        <p class="app-footer__notice">
          Frontend prototype, simulation only — no live registration.
        </p>
      </div>

      <div class="app-footer__labels">
        <span>DATA PRIVACY MANUAL</span>
        <span>SYSTEM TERMS</span>
        <span>STATIONERY SPEC 03-A</span>
      </div>
    </footer>
  </q-layout>
</template>

<style scoped lang="scss">
// Letterhead world: white paper, maroon rules, documentary serif lockup.
// See .impeccable/surfaces/frontend-src-layouts-mainlayout-vue.md.
.app-header {
  background: var(--color-surface);
  color: var(--color-foreground);
  border-bottom: 1px solid var(--color-border);
}

.letterhead__band {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--spacing-3) var(--spacing-6);
  padding: var(--spacing-4) var(--spacing-4) var(--spacing-3);
}

.letterhead__identity {
  display: flex;
  align-items: center;
  gap: var(--spacing-3);
  min-width: 0;
}

.letterhead__seal {
  color: var(--color-secondary);
  flex: none;
}

.letterhead__name {
  font-family: var(--font-serif);
  font-size: var(--text-subhead);
  font-weight: 700;
  line-height: var(--leading-tight);
  letter-spacing: 0.02em;
  text-transform: uppercase;
  color: var(--color-secondary);
  margin: 0;
}

.letterhead__window {
  font-size: var(--text-caption);
  font-weight: 600;
  letter-spacing: var(--tracking-eyebrow);
  text-transform: uppercase;
  color: var(--color-foreground-muted);
  margin: 3px 0 0;

  // The acronym expansion ("Nexus for Identity-verification…") is four words
  // of supporting copy — the first thing to give up when horizontal room is
  // scarce. It returns at 640px, where the band stops wrapping. Navigation is
  // never collapsed: there are exactly two destinations (Register, Admin), so
  // both stay on the bar at every width rather than hiding behind a drawer.
  display: none;
}

.letterhead__nav {
  display: flex;
  align-items: stretch;
  gap: var(--spacing-4);
  margin-left: auto;
}

.letterhead__link {
  min-height: var(--touch-target);
  // No --spacing-5 on the 4px scale (1/2/3/4/6/8/12/16): --spacing-4 (16px) is
  // the nearest step up from spacing-3. An undefined var() would invalidate
  // the whole declaration and drop the links to zero padding.
  padding: 0 var(--spacing-4);
  border-radius: 0;
  background: none;
  color: var(--color-foreground);
  font-size: var(--text-caption);
  font-weight: 600;
  letter-spacing: var(--tracking-eyebrow);
  text-transform: uppercase;
  text-decoration: none;
  transition:
    color var(--duration-fast) var(--ease-out),
    background-color var(--duration-fast) var(--ease-out);

  // Quasar's action layer has no place on printed matter.
  &::before {
    display: none;
  }
}

// Ledger tab: hover washes the whole touch target, the claim segment
// below marks active — no underline, no weight jump.
.letterhead__link:hover {
  color: var(--color-secondary);
  background: color-mix(in srgb, var(--color-secondary) 8%, transparent);
}

.letterhead__link:focus-visible {
  color: var(--color-secondary);
  outline: 2px solid var(--color-secondary);
  outline-offset: -2px;
}

.letterhead__link.is-active {
  color: var(--color-secondary);
}

.letterhead__rule {
  position: relative;
  height: 6px;

  &::before {
    content: "";
    position: absolute;
    inset: auto 0 0 0;
    height: 2px;
    background: var(--color-secondary);
  }
}

// Fused tab: the rule locally thickens under the active link,
// gilded with a 1px seal-gold edge.
.letterhead__claim {
  position: absolute;
  top: 0;
  left: 0;
  height: 6px;
  background: var(--color-secondary);

  &.is-live {
    transition:
      transform var(--duration-base) var(--ease-out),
      width var(--duration-base) var(--ease-out);
  }

  &::after {
    content: "";
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    height: 1px;
    background: var(--color-accent);
  }
}

.app-main {
  max-width: var(--measure-max);
  margin: 0 auto;
  padding: var(--spacing-6) var(--spacing-4) var(--spacing-12);
}

.app-footer {
  align-items: baseline;
  border-top: 1px solid var(--color-border);
  color: var(--color-foreground-muted);
  display: flex;
  flex-wrap: wrap;
  font-size: var(--text-caption);
  gap: var(--spacing-4) var(--spacing-6);
  justify-content: space-between;
  line-height: var(--leading-caption);
  padding: var(--spacing-6) var(--spacing-4);
  text-align: left;
}

// Left block: two-line stationery identity. Its baseline is the org line's
// first line box, so the mark, the org text and the labels across the gap
// all sit on one rule; the column gap carries the second line beneath.
.app-footer__identity {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-2);
}

// Maroon square — a --spacing-3 box in secondary ink. As an empty
// inline-block its baseline is its bottom edge, so align-items: baseline
// on the footer parks it on the org line like a bullet on the rule.
.app-footer__mark {
  background: var(--color-secondary);
  display: inline-block;
  height: var(--spacing-3);
  margin-right: var(--spacing-3);
  width: var(--spacing-3);
}

.app-footer__org,
.app-footer__notice {
  margin: 0;
}

// Right block: three stationery labels — plain spans, deliberately not
// links (spec §6.6: dead links are worse than labels). Mono caption,
// tracked caps, muted — contrast measured at Task 10.
.app-footer__labels {
  color: var(--color-foreground-muted);
  display: flex;
  flex-wrap: wrap;
  font-family: var(--font-mono);
  gap: var(--spacing-3) var(--spacing-4);
  letter-spacing: var(--tracking-eyebrow);
  text-transform: uppercase;
}

@media (min-width: 640px) {
  .letterhead__band {
    flex-wrap: nowrap;
    padding: var(--spacing-4) var(--spacing-8) var(--spacing-3);
  }

  // Restore the expansion now that the band is a single row and has room.
  .letterhead__window {
    display: block;
  }
}

@media (min-width: 1024px) {
  .app-main {
    padding: var(--spacing-8) var(--spacing-6) var(--spacing-12);
  }
}
</style>
