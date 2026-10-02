# ADR-0002: Per-term data lifecycle — archive & reset

**Status:** Accepted — 2026-10-02 (grilled interview, user decision)

## Context

The schema has no term dimension: `registrations` dedupes `student_number`
across all time, so "the roster" is everyone who ever registered. The org's
real model: **membership is per-semester — members re-register each term**
(year levels advance, members graduate/leave, dues reset).

Pressure-test result: "accumulate forever" avoids nothing — the moment an
export must answer "who is active *this* semester?" a term marker is required
anyway, while stale rows keep polluting every query and ex-member artifacts
are retained without purpose (RA 10173 purpose-limitation liability).

## Decision

- Members re-register each semester; the roster is **the current term's**
  registrations.
- Add `term` to the data model. Scope the dedupe window function, admin
  stats, and CSV export to the current term.
- Old terms stay **read-only, labeled history**. Advancing to a new semester
  = advancing the current term (reset), not deleting data.
- A purge/retention schedule for old terms is a later decision.

## Consequences

- Reset operation is cheap: set current term, seed fresh; queries are
  term-scoped everywhere.
- PRD's "closed window" lifecycle maps onto terms.
- Enters scope at wiring time: schema migration + term-aware admin UI.
- **Ref-ID sequencing (decided 2026-10-02):** `REG-YYYY-NNNNN` keeps its
  format; the NNNNN sequence runs through each calendar year and continues
  across terms — unique forever, no format churn.
- **Term label (decided 2026-10-02):** `AY 2026-27 S1` style — how the org
  already speaks; used in UI, exports, and seed data.
- **Tenancy (decided 2026-10-02):** single org in pass 1 — no `org_id`.
  "Keep it open for expansion" = keep all data access centralized (one
  repository layer, no scattered single-row assumptions) so a future
  `org_id` migration stays one contained change. Deliberate: accept that
  churn *if* expansion happens, don't pay for it now.
- Open sub-decisions — all resolved 2026-10-02:
  - **Term switcher:** no switcher UI — one `current_term` (settings row),
    displayed read-only in the admin console; advancing a term = CLI command.
  - **Purge schedule:** manual CLI purge only; no automation until a real
    retention policy exists.
