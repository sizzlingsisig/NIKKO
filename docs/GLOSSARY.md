# Glossary

Domain terms for Form5 Portal (NIKKO). Wording here is binding for code,
UI copy, and docs. Add a term when a decision gives it precise meaning.

## Domain

- **Form 5** — the UP enrollment form (PDF) a student uploads; source of the
  6 roster fields. Never "form5" in prose (code identifiers excepted).
- **Term (semester)** — unit of roster lifecycle. Members re-register each
  term; dedupe, stats, and export are always term-scoped (ADR-0002).
  Written `AY 2026-27 S1` in UI, exports, and seed data. Replaces PRD's
  "registration window".
- **Archive & reset** — term lifecycle: old terms remain read-only history;
  a new semester = advancing the current term, not deleting data.
- **Roster** — the deduplicated member list of the **current term**; the
  CSV export product.
- **Dedupe** — collapse to the latest submission per student
  (`ROW_NUMBER() OVER (PARTITION BY student_number ...) = 1`), scoped to the
  current term. Admins see raw vs collapsed rows (dedupe transparency).
- **Reference ID** — `REG-YYYY-NNNNN`, the single confirmation handed on
  submit ("one shot, one receipt"). Cross-term sequencing is an open
  decision (ADR-0002).
- **Student number** — the dedup key; format validated on the form.
- **College codes** — SBM / CAS / CFOS / SOT. **Mail domain** — `@up.edu.ph`
  only.

## Pipeline & storage

- **Pass 1 (E2E pass)** — first milestone: real digital text-layer PDF →
  client-side parse → Garage → DB row → dedupe → CSV export, plus real admin
  auth and the 7-day orphan sweeper. Excludes OCR and XLSX (ADR-0001).
- **Milestone 2** — OCR for scanned inputs (tesseract.js, client-side) with
  confidence threshold and forced review below 75%.
- **Client-side parsing** — binding RA 10173 claim: extraction and previews
  never leave the device. Binding regardless of input type; OCR stages
  *coverage*, never the location, of parsing.
- **Artifacts** — form5 / photo / signature files. Garage (S3) holds bytes,
  DB holds keys — never full URLs.
- **Presigned URL** — short-lived signed PUT/GET minted by the API; bucket
  stays private. Known issue: PUT URLs use the compose-internal hostname and
  are not browser-reachable from the host.
- **Admin** — a named console account. Seed-only provisioning (CLI/env; no
  signup UI), password → **12h sliding** session cookie, all equal, no
  roles (ADR-0003).
- **Degree program** — value from the static typed list in
  `frontend/src/domain/` (decided 2026-10-02); no free text.
- **Simulation badge** — visible marker that a surface is mocked; removing
  or faking it violates the honest-prototype principle.

## Milestone boundary & standing decisions (2026-10-02)

- **In pass 1:** digital-PDF parsing, full upload chain, real admin auth
  (seeded multi-admin, ADR-0003), orphan sweeper, consent reword covering
  server-side retention.
- **Deferred:** OCR (= milestone 2), XLSX export (CSV only), artifact
  viewer (= milestone 1.5, required before first real registration),
  theme re-skin (after E2E; maroon prototype theme stands), purge (manual
  CLI only), **hosting** (localhost until pass 1 is green; one-box VPS
  with the existing compose stack is the leading candidate).
- **Term operations:** advancing = CLI command (`current_term` shown
  read-only in the admin console — no switcher UI).
- **Database:** SQLite (WAL) for pass 1 — PRD §7 DB question closed;
  Postgres only revisited together with the hosting decision.
- **Ref-ID:** `REG-YYYY-NNNNN`, per-calendar-year sequence continuing across
  terms (ADR-0002).
- **Tenancy:** single org in pass 1 (no `org_id`); data access stays
  centralized so a future expansion migration is contained (ADR-0002).
