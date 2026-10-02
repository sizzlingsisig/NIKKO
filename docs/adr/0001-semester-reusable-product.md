# ADR-0001: Semester-reusable product (drop the Q1 2027 window framing)

**Status:** Accepted — 2026-10-02 (grilled interview, user decision)

## Context

`PRODUCT.md` and `PRD.md` assumed a time-boxed Q1 2027 registration window. The
user's actual intent: a tool the org reuses **throughout semesters**, with no
single-window production deadline. Time budget is **3–5 hrs/week**, and the one
success test for the near term is **everything wired end-to-end**: real PDF
parsed → artifact stored in Garage → DB row → dedupe → CSV export.

## Decision

- The Q1 2027 window framing stops being a driving constraint; the app targets
  recurring per-semester use.
- Primary success test: one full end-to-end chain works with real data.
- Scope is governed by the 3–5 hrs/week budget; deferrals are recorded as
  explicit milestone boundaries, not re-litigated.

## Consequences

- PRD's window-lifecycle language becomes the per-semester "term" concept
  (ADR-0002).
- Milestone boundaries set 2026-10-02:
  - **In pass 1:** client-side parsing of digital text-layer PDFs, the full
    upload chain, real admin auth, 7-day orphan sweeper, and the consent
    reword covering server-side retention (RA 10173 — before the first real
    artifact is stored).
  - **Deferred:** OCR (scanned inputs) = milestone 2; XLSX export = later
    (CSV only); theme re-skin (pine-teal production palette) = after the
    E2E chain is green — maroon prototype theme stands until then; the
    gated artifact viewer = milestone 1.5, **required before the first
    real registration** (localhost phase means nobody submits for real yet).
- The client-side parsing claim (RA 10173, "privacy by mechanism") remains
  binding. "Both scans and digital inputs" is a coverage target staged behind
  the OCR milestone — where parsing runs never changes.
- PRD §7 open questions still live: hosting, DB choice, term/ref-ID specifics.
