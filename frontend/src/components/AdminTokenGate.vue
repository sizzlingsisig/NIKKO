<script setup lang="ts">
import { onBeforeUnmount, ref } from "vue";

import AppCard from "@/components/AppCard.vue";

const emit = defineEmits<{ submit: [token: string] }>();

const token = ref("");
const localError = ref("");
const verified = ref(false);

// The parent swaps this gate for the console the instant it receives
// `submit`, so the verified stamp is pressed first and the event follows
// after it has had time to paint — otherwise that state could never be
// seen. One short authored hold (not content the user is waiting on),
// cancelled if the component leaves before it fires.
const VERIFY_HOLD_MS = 700;
let holdTimer: ReturnType<typeof setTimeout> | undefined;

function submit() {
  if (verified.value) return;
  if (token.value.trim().length === 0) {
    localError.value = "Enter a demo token (any value).";
    return;
  }
  localError.value = "";
  verified.value = true;
  holdTimer = setTimeout(() => emit("submit", token.value), VERIFY_HOLD_MS);
}

onBeforeUnmount(() => {
  if (holdTimer !== undefined) clearTimeout(holdTimer);
});
</script>

<template>
  <AppCard
    eyebrow="FR-4.1"
    title="Admin Access"
    subtitle="Administrative routes are token-gated. Enter any demo token to simulate authentication."
  >
    <!-- Counterfoil stub: the entry line sits on sunken stock under a
         perforated edge, ready to tear off into the console. -->
    <q-form v-if="!verified" class="token-gate" novalidate @submit="submit">
      <div class="token-gate__stub">
        <div class="token-gate__row">
          <q-input
            v-model="token"
            label="Admin token"
            placeholder="ADMIN-TOKEN-XXXX"
            autocomplete="off"
            spellcheck="false"
            outlined
            dense
            hide-bottom-space
            input-class="token-gate__input"
            class="token-gate__field"
            :error="Boolean(localError)"
            :error-message="localError"
            @keyup.enter="submit"
          />
          <q-btn
            type="submit"
            unelevated
            color="primary"
            label="Sign in"
            class="token-gate__submit"
          />
        </div>
      </div>
    </q-form>

    <!-- Verified: rubber stamp lands on the stub, announced to screen
         readers, then the hand-off to the console follows it. -->
    <p v-else class="token-gate__stamp type-eyebrow" role="status">
      <q-icon name="check" size="16px" />
      <span>Verified</span>
    </p>
  </AppCard>
</template>

<style scoped lang="scss">
// Torn-from-the-book stub: sunken stock, perforation ruling its top edge.
// Decorative 1px borders only — elevation is declared once.
.token-gate__stub {
  background: var(--color-surface-sunken);
  border: var(--border-hairline) solid var(--color-rule-hairline);
  border-top: var(--border-perforation);
  max-width: 100%;
  padding: var(--spacing-4);
  width: fit-content;
}

.token-gate__row {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-start;
  gap: var(--spacing-3);
  max-width: 32rem;
}

.token-gate__field {
  flex: 1 1 14rem;
}

.token-gate__submit {
  margin-top: 0;
}

// Touch floor: Quasar's dense control is 40px; the stub's entry line
// reaches the 44px target without leaving dense density.
.token-gate :deep(.q-field--dense .q-field__control) {
  height: var(--touch-target);
}

// Focus = amber hairline hard against ink (AppCard's measured pair:
// amber/ink 7.90:1; amber never sits alone on paper, 1.73:1). Error keeps
// its red rule, so :not(.q-field--error) guards the ink swap.
.token-gate
  :deep(
    .q-field--outlined.q-field--focused:not(.q-field--error)
      .q-field__control:before
  ) {
  border-color: var(--color-foreground);
}

// The amber ring rides just outside the ink rule; height:auto lets the
// inset box stretch under it (Quasar pins :after height for outlined).
.token-gate :deep(.q-field--outlined.q-field--focused .q-field__control:after) {
  border-color: var(--color-rule-focus);
  border-radius: 0; // square ring — matches the square control it wraps
  bottom: -2px;
  height: auto;
  left: -2px;
  right: -2px;
  top: -2px;
}

// The global teal :focus-visible ring would land inside this control as a
// second, competing indicator — ink + amber is this field's focus state.
.token-gate :deep(.q-field__input:focus-visible) {
  outline: none;
}

// Tokens are machine-generated, not prose — render them in the mono stack.
// :deep because the native input lives inside QInput's subtree, where the
// scope attribute never reaches.
.token-gate :deep(.token-gate__input) {
  font-family: var(--font-mono);
  font-size: var(--text-body);
}

// Rubber stamp: tracked small caps maroon on its tint (9.51:1), square
// cut, pressing once from just oversized (exponential ease-out; the
// default state under reduced motion is fully visible).
// .type-eyebrow carries the register; this rule keeps the cell and the press.
.token-gate__stamp {
  align-items: center;
  animation: token-gate-stamp var(--duration-fast) var(--ease-out) both;
  background: var(--color-stamp-bg);
  border: var(--border-hairline) solid var(--color-stamp);
  color: var(--color-stamp);
  display: inline-flex;
  gap: var(--spacing-2);
  margin: 0;
  padding: var(--spacing-2) var(--spacing-4);
}

@keyframes token-gate-stamp {
  from {
    opacity: 0;
    transform: scale(1.06);
  }

  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
