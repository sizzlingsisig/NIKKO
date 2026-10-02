import { defineStore } from "pinia";
import { computed, ref } from "vue";

/**
 * Admin session. The prototype accepts any non-empty token to simulate
 * authentication (FR-4.1); the real scheme is an open PRD question.
 */
export const useAdminStore = defineStore("admin", () => {
  const token = ref("");
  const isAuthenticated = computed(() => token.value.length > 0);

  function signIn(candidate: string): boolean {
    const trimmed = candidate.trim();
    if (trimmed.length === 0) return false;
    token.value = trimmed;
    return true;
  }

  function signOut(): void {
    token.value = "";
  }

  return { token, isAuthenticated, signIn, signOut };
});
