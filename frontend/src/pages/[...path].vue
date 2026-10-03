<template>
  <div
    class="fullscreen bg-secondary text-white text-center q-pa-md flex flex-center"
  >
    <div>
      <div class="not-found__numeral">404</div>

      <div class="not-found__title">Oops. Nothing here...</div>

      <q-btn
        class="q-mt-xl"
        color="white"
        text-color="secondary"
        unelevated
        to="/register"
        label="Go Home"
        no-caps
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
// The decorative numeral inherits body's fixed 24px leading, which would
// collapse its line box and pull the title/button up into the glyphs.
// --leading-none is now pinned explicitly: delete that line-height and the
// collapse above returns. --text-numeral must also stay out-scaling
// --text-title — that is the whole reason this numeral is not --text-title.
.not-found__numeral {
  font-size: var(--text-numeral);
  line-height: var(--leading-none);
}

// Faded, but never so far that it drops under the 3:1 large-text floor
// against the maroon ground (0.4 measured 1.6:1, 0.62 measures 4.9:1).
.not-found__title {
  font-family: var(--font-serif);
  font-size: var(--text-title);
  font-weight: var(--weight-bold);
  line-height: var(--leading-tight);
  opacity: 0.62;
}
</style>
