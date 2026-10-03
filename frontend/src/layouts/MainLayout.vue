<script setup lang="ts">
import { computed, nextTick, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";

import AppCrest from "@/components/AppCrest.vue";

const route = useRoute();

const NAV_ITEMS = [
  { label: "Register", to: "/register" },
  { label: "Admin", to: "/admin" }
] as const;

// One claim line serves rest, hover and focus alike: it parks under the
// active route, slides to whichever link is being inspected, and returns
// when the pointer or focus leaves the nav. It only reports state —
// navigation itself stays entirely with the router links.
const navEl = ref<HTMLElement | null>(null);
const claimEl = ref<HTMLElement | null>(null);
const hoveredTo = ref<string | null>(null);
const claimArmed = ref(false);

const activeTo = computed(
  () => NAV_ITEMS.find(item => route.path === item.to)?.to ?? null
);
const claimTo = computed(() => hoveredTo.value ?? activeTo.value);

// Measured, not guessed: DESIGN.md calls for getBoundingClientRect here and
// a re-arm after fonts settle, so the line never slides in from zero on load.
function positionClaim(): void {
  const nav = navEl.value;
  const claim = claimEl.value;
  if (!nav || !claim) return;

  const to = claimTo.value;
  const link = to
    ? nav.querySelector<HTMLElement>(`[data-claim="${to}"]`)
    : null;

  if (!link) {
    // No route matches the nav items — collapse instead of guessing.
    claim.style.opacity = "0";
    claim.style.width = "0px";
    return;
  }

  const navBox = nav.getBoundingClientRect();
  const linkBox = link.getBoundingClientRect();
  // Inset by the link's own horizontal padding: the rule rides the label,
  // not the whole touch target — the same inset the static bar had.
  const inset = parseFloat(getComputedStyle(link).paddingLeft);

  claim.style.opacity = "1";
  claim.style.width = `${Math.max(linkBox.width - inset * 2, 0)}px`;
  claim.style.transform = `translateX(${linkBox.left - navBox.left + inset}px)`;
}

watch(claimTo, () => {
  void nextTick(positionClaim);
});

onMounted(() => {
  positionClaim(); // placed while the transition is still disarmed
  requestAnimationFrame(() => {
    claimArmed.value = true;
  });
  void document.fonts.ready.then(positionClaim);
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
              <h1 class="letterhead__name type-subhead-serif">NIKKO</h1>
              <p class="letterhead__window type-eyebrow">
                Nexus for Identity-verification, Key-signatures, and Kompiled
                Organization-lists
              </p>
            </div>
          </div>

          <nav
            ref="navEl"
            class="letterhead__nav"
            aria-label="Primary"
            @mouseleave="hoveredTo = null"
            @focusout="hoveredTo = null"
          >
            <q-btn
              v-for="item in NAV_ITEMS"
              :key="item.to"
              :to="item.to"
              :label="item.label"
              :data-claim="item.to"
              no-caps
              flat
              unelevated
              class="letterhead__link"
              :class="{ 'is-active': route.path === item.to }"
              @mouseenter="hoveredTo = item.to"
              @focus="hoveredTo = item.to"
            />
            <span
              ref="claimEl"
              class="letterhead__claim"
              :class="{ 'is-armed': claimArmed }"
              aria-hidden="true"
            />
          </nav>
        </div>
      </div>
    </q-header>

    <q-page-container>
      <main class="app-main">
        <slot />
      </main>
    </q-page-container>

    <!-- Footer: the colophon ledger — the maroon rule closes the
         letterhead; three masses share the content column's margins at
         every width: identity, wayfinding, release. -->
    <footer class="app-footer">
      <div class="app-footer__band">
        <div class="app-footer__col">
          <p class="app-footer__org">
            <AppCrest :size="24" class="app-footer__seal" />
            <span class="app-footer__lockup">
              <span class="app-footer__name"
                >University of the Philippines Visayas</span
              >
              <span class="app-footer__office">
                Official property of KOMSAI.ORG
              </span>
            </span>
          </p>
          <p class="app-footer__copy">© 2026 KOMSAI.ORG</p>
        </div>

        <div class="app-footer__col">
          <p class="app-footer__col-label type-eyebrow">Navigate</p>
          <nav class="app-footer__links" aria-label="Footer">
            <router-link
              v-for="item in NAV_ITEMS"
              :key="item.to"
              :to="item.to"
              class="app-footer__link"
              >{{ item.label }}</router-link
            >
          </nav>
        </div>

        <div class="app-footer__col">
          <p class="app-footer__col-label type-eyebrow">Release</p>
          <p class="app-footer__stamp">v1.8.4</p>
          <p class="app-footer__stamp">Last updated 2026-10-02</p>
        </div>
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
  // Caps the band at .app-main's measure (90rem) and centers it, so on
  // viewports wider than 1440px the lockup and nav share the content
  // column's left/right margins instead of staying edge-anchored.
  max-width: var(--measure-max);
  margin: 0 auto;
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
  // Family, size, weight and the tighter serif leading come from
  // .type-subhead-serif. The wordmark keeps its own rule for the two
  // declarations no role covers: it is set in caps like an eyebrow but
  // tracked normal, because a letter-spaced wordmark reads as a label
  // rather than a lockup.
  letter-spacing: var(
    --tracking-normal
  ); // snapped 0.02em in the token migration
  text-transform: uppercase;
  color: var(--color-secondary);
  margin: 0;
}

.letterhead__window {
  color: var(--color-foreground-muted);
  margin: 3px 0 0;
  // .type-eyebrow supplies the whole tracked-caps register. This rule used to
  // omit line-height and inherit the body's --leading-body, so the window line
  // sat in a 24px box; it now takes --leading-caption (16px) like every other
  // caption label. The 3px margin above compensates for the tighter box.
  // Weight snapped 600 -> 700 (.type-eyebrow's) as part of the same change.

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
  // Anchors the claim line: links are the flex children, the line measures
  // itself against this box in script.
  position: relative;
}

.letterhead__link {
  position: relative;
  min-height: var(--touch-target);
  // No --spacing-5 on the 4px scale (1/2/3/4/6/8/12/16): --spacing-4 (16px) is
  // the nearest step up from spacing-3. An undefined var() would invalidate
  // the whole declaration and drop the links to zero padding.
  padding: 0 var(--spacing-4);
  border-radius: 0;
  background: none;
  color: var(--color-foreground);
  // No .type-eyebrow here, deliberately. This is a <q-btn>, and app.scss's
  // global .q-btn rule (16px / 700 / tracking 0 / not uppercase) lands after
  // .type-eyebrow at equal specificity — a role class added here would lose.
  // The scoped rule outranks both, so the eyebrow register stays spelled out.
  // Open drift: line-height is the one bundle declaration missing here, since
  // Quasar's own .q-btn sets line-height on this box and overriding it would
  // change the button's height, not just its label's. Left for a human call
  // rather than snapped blind.
  font-size: var(--text-caption);
  font-weight: var(--weight-bold);
  letter-spacing: var(--tracking-eyebrow);
  text-transform: uppercase;
  text-decoration: none;
  transition: color var(--duration-fast) var(--ease-out);

  // Quasar's action layer has no place on printed matter.
  &::before {
    display: none;
  }
}

// Ledger tab: hover inks the label maroon — the claim line below carries the
// rest of the feedback. No wash, no weight jump.
.letterhead__link:hover {
  color: var(--color-secondary);
}

.letterhead__link:focus-visible {
  color: var(--color-secondary);
  outline: 2px solid var(--color-secondary);
  outline-offset: -2px;
}

.letterhead__link.is-active {
  color: var(--color-secondary);
}

// The claim line: one 2px maroon segment, gilded with a 1px seal-gold
// hairline, serves rest, hover and focus alike — it parks under the active
// route, slides to the link being inspected, and returns on leave. Script
// measures the parked positions (getBoundingClientRect) and arms the
// transition only after the first placement, per DESIGN.md, so the line
// never slides in from zero on load. pointer-events keeps it out of the
// links' hit testing.
.letterhead__claim {
  background: var(--color-secondary);
  bottom: 0;
  height: 2px;
  left: 0;
  opacity: 0;
  pointer-events: none;
  position: absolute;
  transform: translateX(0);
  width: 0;

  &::after {
    content: "";
    position: absolute;
    inset: auto 0 0 0;
    height: 1px;
    background: var(--color-accent);
  }
}

.letterhead__claim.is-armed {
  transition:
    transform var(--duration-base) var(--ease-out),
    width var(--duration-base) var(--ease-out),
    opacity var(--duration-fast) var(--ease-out);
}

@media (prefers-reduced-motion: reduce) {
  .letterhead__claim.is-armed {
    transition: none;
  }
}

.app-main {
  max-width: var(--measure-max);
  margin: 0 auto;
  padding: var(--spacing-6) var(--spacing-4) var(--spacing-12);
}

// The colophon: paper white closed by the letterhead's own device — the
// 2px maroon rule. DESIGN.md reserves 2px for horizontal ruled lines and
// the strong rule closes a block; the claim line opened the sheet, this
// one signs it off.
.app-footer {
  background: var(--color-surface);
  border-top: 2px solid var(--color-secondary);
  color: var(--color-foreground-muted);
  font-size: var(--text-caption);
  line-height: var(--leading-caption);
  text-align: left;
}

// Capped like .letterhead__band (16px sides, 24px at ≥1024px) with the
// room a colophon needs: three ledger masses spread across the measure —
// identity, wayfinding, release — wrapping as a unit on narrow sheets.
.app-footer__band {
  align-items: flex-start;
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-6) var(--spacing-8);
  justify-content: space-between;
  margin: 0 auto;
  max-width: var(--measure-max);
  padding: var(--spacing-6) var(--spacing-4) var(--spacing-8);
}

// Every column is a stack: label first, mass beneath.
.app-footer__col {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-2);
  min-width: 0;
}

// Column labels in the letterhead's meta register — the same tracked caps
// as the nav links and window line. Muted, 6.00:1 on paper.
//
// .type-eyebrow supplies the whole tracked-caps register on both labels
// ("Navigate" and "Release"), so weight/tracking/uppercase are spelled out
// nowhere. .app-footer already sets caption size on --leading-caption, which
// is exactly what .type-eyebrow sets, so the swap is weight-only here: the
// raw 600 snapped to 700 (.type-eyebrow's). This rule keeps colour and margin.
.app-footer__col-label {
  color: var(--color-foreground-muted);
  margin: 0;
}

// Wayfinding: the two real destinations as plain router links — ink bold
// with the header link's ink on hover/focus, 24px targets, and the active
// route resting maroon like the header's claim line.
//
// No role class: these are sentence-case links, so .type-eyebrow would
// uppercase them, and .type-meta would drop them to 400 — flattening two
// destinations into the muted fine print they are meant to stand out from.
.app-footer__links {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-1);
}

.app-footer__link {
  color: var(--color-foreground);
  // Snapped 600 -> 700. Only two weights exist (Libre Caslon ships 700-only,
  // JetBrains Mono 400-only); 700 keeps these two links the same voice as the
  // header's .letterhead__link and still ahead of the office line beneath.
  font-weight: var(--weight-bold);
  padding: 2px 0;
  text-decoration: none;
  transition: color var(--duration-fast) var(--ease-out);
}

.app-footer__link:hover {
  color: var(--color-secondary);
}

.app-footer__link:focus-visible {
  color: var(--color-secondary);
  outline: 2px solid var(--color-secondary);
  outline-offset: 2px;
}

.app-footer__link.router-link-active {
  color: var(--color-secondary);
}

// Copyright line: legal fine print — sans, not machine evidence.
.app-footer__copy {
  color: var(--color-foreground-muted);
  margin: 0;
}

// Seal + two-line lockup — the official signature block. The 24px seal
// centers against the two text rules and tints maroon like the header's.
.app-footer__org {
  align-items: center;
  display: flex;
  gap: var(--spacing-3);
  margin: 0;
  min-width: 0;
}

.app-footer__seal {
  color: var(--color-secondary);
  flex: none;
}

.app-footer__lockup {
  display: flex;
  flex-direction: column;
}

// Hierarchy by weight, not size: issuer leads ink bold, the office line
// trails muted beneath (8.9:1 / 6.00:1 on paper).
.app-footer__name {
  color: var(--color-foreground);
  // Snapped 600 -> 700. The hierarchy the comment describes is weight-based,
  // so it has to survive the snap: 700 keeps the issuer above the office line,
  // which inherits the footer's 400.
  font-weight: var(--weight-bold);
}

.app-footer__office {
  color: var(--color-foreground-muted);
}

// Release stamp: the strings a machine produced, so they earn mono —
// tabular figures for version and date (Mono-As-Evidence). Muted,
// 6.00:1 on paper.
.app-footer__stamp {
  font-family: var(--font-mono);
  font-variant-numeric: tabular-nums;
  margin: 0;
}

@media (min-width: 640px) {
  .letterhead__band {
    flex-wrap: nowrap;
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

  // Horizontal padding tracks .app-main at every breakpoint (16px below,
  // 24px here) so the lockup and nav items share the content column's
  // left/right margins instead of sitting 32px in.
  .letterhead__band {
    padding: var(--spacing-4) var(--spacing-6) var(--spacing-3);
  }

  // The footer band tracks the same horizontal pad as the header band.
  .app-footer__band {
    padding: var(--spacing-6) var(--spacing-6) var(--spacing-8);
  }
}
</style>
