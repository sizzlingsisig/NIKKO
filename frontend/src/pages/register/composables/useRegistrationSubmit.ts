import { computed, onBeforeUnmount, ref, type Ref } from "vue";

import type { Attachment, RegistrationDraft } from "@/domain/registration";
import { EMPTY_DRAFT } from "@/domain/registration";
import { isDraftValid } from "@/domain/validation";
import { useRosterStore } from "@/stores/roster";

interface SubmitContext {
  /** Shared reactive draft; the store refuses anything `isDraftValid` rejects. */
  draft: RegistrationDraft;
  photo: Ref<Attachment | null>;
  signature: Ref<Attachment | null>;
  consent: Ref<boolean>;
  revealErrors: Ref<boolean>;
  /** Toast reporter — injected so this module stays free of UI details. */
  notify: (message: string) => void;
  /** Called with the stored reference id once the mock commit lands. */
  onSubmitted: (referenceId: string) => void;
}

/**
 * Owns the submit side of the flow (FR-2 -> FR-3): validation gating, the
 * mock atomic commit and the FR-2.4 release of volatile submission data.
 *
 * The draft, attachments and consent live with the caller (the page) because
 * the review step renders them; only the submit lifecycle is owned here.
 */
export function useRegistrationSubmit(ctx: SubmitContext) {
  const roster = useRosterStore();
  const isSubmitting = ref(false);

  let commitTimer: ReturnType<typeof setTimeout> | null = null;

  function cancelCommit() {
    if (commitTimer !== null) {
      clearTimeout(commitTimer);
      commitTimer = null;
    }
  }

  onBeforeUnmount(cancelCommit);

  const attachmentsComplete = computed(() =>
    Boolean(ctx.photo.value && ctx.signature.value)
  );

  const canSubmit = computed(
    () =>
      isDraftValid(ctx.draft) && attachmentsComplete.value && ctx.consent.value
  );

  function onSubmit() {
    ctx.revealErrors.value = true;

    if (!isDraftValid(ctx.draft)) {
      ctx.notify("Please fix the highlighted fields.");
      return;
    }
    if (!attachmentsComplete.value) {
      ctx.notify("Photo and signature are both required.");
      return;
    }
    if (!ctx.consent.value) {
      ctx.notify("RA 10173 consent is required.");
      return;
    }

    isSubmitting.value = true;
    // Stands in for the backend's atomic WAL commit (<= 35 ms).
    cancelCommit();
    commitTimer = setTimeout(() => {
      commitTimer = null;
      const referenceId = roster.addRegistration({ ...ctx.draft });
      isSubmitting.value = false;
      if (referenceId === null) {
        // Unreachable while the guard above holds; the store refuses to write
        // an unvalidated draft, so surface it rather than showing a false ack.
        ctx.notify("Please fix the highlighted fields.");
        return;
      }
      ctx.onSubmitted(referenceId);
    }, 30);
  }

  /**
   * FR-2.4: revoke blob previews and clear every trace of the submission
   * payload (attachments, consent, draft, error flags).
   */
  function releaseSubmission() {
    for (const attachment of [ctx.photo.value, ctx.signature.value]) {
      if (attachment?.url.startsWith("blob:"))
        URL.revokeObjectURL(attachment.url);
    }
    ctx.photo.value = null;
    ctx.signature.value = null;
    ctx.consent.value = false;
    Object.assign(ctx.draft, EMPTY_DRAFT);
    ctx.revealErrors.value = false;
  }

  /** Aborts a pending mock commit and resets the submitting flag. */
  function resetSubmit() {
    cancelCommit();
    isSubmitting.value = false;
  }

  return { isSubmitting, canSubmit, onSubmit, releaseSubmission, resetSubmit };
}
