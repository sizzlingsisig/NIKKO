# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

- **Registrants (primary):** UPV students holding their Form 5 PDF during a
  registration window. Job: get their roster data into the org roster fast —
  without re-typing — and receive a single confirmation ID.
- **Org admins (secondary):** roster managers who need a token-gated console
  to review submissions, collapse duplicates, and export a deduplicated roster
  (CSV/XLSX).

## Product Purpose

Digitize UPV student-organization member intake. Students upload a UP Form 5
(PDF); the portal extracts 6 roster fields in-browser, the student
verifies/corrects and attaches photo + signature under RA 10173 consent, then
receives a reference ID (`REG-YYYY-NNNNN`). Admins export a deduplicated roster
(latest submission per student). Success = fast upload, pre-filled form, one
confirmation ID, zero re-typed roster data, no silent data loss.

## Positioning

Privacy by mechanism, not by policy: field extraction runs on-device
(in-browser), so sensitive Form 5 content never leaves the student's device
during parsing. Server-side, only pointers + consented artifacts exist — S3
holds bytes, DB holds keys — so RA 10173 erasure is a one-prefix delete. A
server-parsing competitor cannot truthfully make the same on-device claim.

## Operating Context

- UPV Student Organization Registration — **Q1 2027 window** (time-boxed
  registration windows, not a always-on service).
- Students arrive with a Form 5 PDF (digital or scanned); scan path uses OCR
  with a confidence threshold and forced manual review below 75%.
- Current build is a **prototype/simulation**: no real PDF parsing shipped, no
  network requests, no persistence; a visible `Simulation` badge in the header
  marks this and must not imply live service.
- Self-hosted **Garage** (S3-compatible) for artifact storage, dev and prod;
  plain S3 API so the provider is an env flip.
- Admin console gated by a demo token (real auth is out of scope for now).

## Capabilities and Constraints

- **In scope:** Register view (3 steps: upload/parse → review/correct →
  submit/acknowledge), Admin view (login → dashboard → export), artifact
  storage per FR-5.
- **Out of scope:** real auth, ID collation (FR-6, planned), payment flows.
- **Privacy (RA 10173, hard constraint):** parsing + previews 100%
  client-side; production = private bucket, SSE at rest, TLS, presigned-only
  serving, consent reword covering server-side retention, retention + erasure
  path.
- **Limits:** PDF ≤ 10 MB; photo/signature JPG/PNG ≤ 5 MB each.
- **Performance budgets:** vector parse ≤ 400 ms; simulated WAL commit ≤ 35 ms.
- **Terminology:** "Form 5" (the UP enrollment form), "reference ID"
  (`REG-YYYY-NNNNN`), "dedupe: latest submission per student", colleges
  SBM/CAS/CFOS/SOT, `@up.edu.ph` mail only.
- **Product name:** **NIKKO** (expansion: *Nexus for Identity-verification,
  Key-signatures, and Kompiled Organization-lists*; user-confirmed).
  Supersedes "New Integrated Kampus Kartsilyo Online", which superseded
  "UPV Org Registration", which itself superseded the long header title
  "Form 5 Member Ingestion Portal".
- Open decisions (recorded, not invented): backend hosting, real admin auth
  scheme, OCR engine choice, ref-ID sequencing, XLSX generator, authoritative
  degree-program list, FR-6 ID card format.

## Brand Commitments

- **UP Visayas seal + identity must be preserved** (binding, user-confirmed).
  Seal asset: `frontend/src/assets/250px-UP_Visayas_Logo.svg.svg`, rendered
  inline via `frontend/src/components/AppCrest.vue`.
- Product name: "NIKKO" — *Nexus for Identity-verification, Key-signatures,
  and Kompiled Organization-lists*.
- No other binding identity constraints were confirmed; visual world beyond
  the seal is open.

## Evidence on Hand

- `PRD.md` — authoritative requirements (FR-1…FR-5, data model, NFRs);
  user-confirmed accurate as of this session.
- `COMMANDS.md`, `frontend/README.md`.
- Working prototype code: `frontend/` (Quasar/Vue 3 SPA, pages
  `register.vue` / `admin.vue`), `backend/` (FastAPI), `bruno/` API collection.
- Seed roster data incl. deliberate duplicate rows (typo re-submission) for
  demoing the dedupe window function.
- **Absences that must not be fabricated:** no real user research, no
  testimonials, no customers, no benchmarks, no launch date; prototype has no
  real parsing/network/persistence.

## Product Principles

1. **Privacy by mechanism** — sensitive parsing happens on-device; never trade
   RA 10173 posture for convenience.
2. **One shot, one receipt** — the student submits once and leaves with a
   single reference ID; no ambiguous outcomes.
3. **Fail visible, never silent** — pending/duplicate/low-confidence states
   surface to humans (admins, forced review) instead of being dropped.
4. **Honest prototype** — simulation limits are labeled; never imply
   capabilities the build does not have.
5. **Dedupe transparency** — admins see raw vs collapsed rows and why; trust
   comes from showing the collapse, not hiding it.

## Accessibility & Inclusion

- Keyboard-operable dropzone, `aria-live` parse log, labelled inputs (PRD
  NFR).
- WCAG contrast is a standing requirement: the theme is described as
  "WCAG-fixed" with measured (not estimated) contrast pairs, and any future
  color work must keep AA as the floor.
- Audience includes first-time form filers under time pressure (registration
  window) — errors must be specific and corrective.
