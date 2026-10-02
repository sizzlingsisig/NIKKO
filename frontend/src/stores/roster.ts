import { defineStore } from "pinia";
import { computed, ref } from "vue";

import { generateRef, nextRowId, SEED_ROWS } from "@/domain/mockData";
import { annotateRoster, computeStats, sortRoster } from "@/domain/roster";
import type { RegistrationDraft, RosterRow } from "@/domain/registration";
import { toCollege } from "@/domain/registration";

/**
 * In-memory roster.
 *
 * The prototype's behaviour is reproduced exactly: the seed rows are the
 * roster at load, a successful submit pushes a row, and the admin console
 * reflects it in real time. Nothing persists and nothing leaves the browser —
 * the real API replaces this store wholesale in a later pass.
 */
export const useRosterStore = defineStore("roster", () => {
  const rows = ref<RosterRow[]>([...SEED_ROWS]);

  const annotated = computed(() => sortRoster(annotateRoster(rows.value)));
  const stats = computed(() => computeStats(rows.value));

  /**
   * Applies a validated draft and returns the freshly minted reference ID.
   *
   * Returns `null` when the draft has not been validated — the college slot is
   * the one field whose type is narrower than `string`, and it is narrowed here
   * rather than cast, so the store never writes a row it would not accept back.
   */
  function addRegistration(draft: Readonly<RegistrationDraft>): string | null {
    const college = toCollege(draft.college);
    if (college === null) return null;

    const ref = generateRef();
    rows.value = [
      ...rows.value,
      {
        id: nextRowId(rows.value),
        student_number: draft.student_number.trim(),
        full_name: draft.full_name.trim(),
        degree_program: draft.degree_program.trim(),
        college,
        year_level: Number.parseInt(draft.year_level, 10),
        up_mail: draft.up_mail.trim(),
        submitted_at: `${new Date().toISOString().slice(0, 19)}Z`,
        ref
      }
    ];
    return ref;
  }

  function resetRoster(): void {
    rows.value = [...SEED_ROWS];
  }

  return { rows, annotated, stats, addRegistration, resetRoster };
});
