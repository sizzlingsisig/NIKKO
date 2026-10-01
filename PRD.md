# Form 5 Member Ingestion Portal — PRD

> Source: `form5_portal_prototype.html` (664-line frontend simulation,
> UPV Student Organization Registration — Q1 2027 Window).
> Status: prototype only — no real PDF parsing, no network requests,
> no data persisted.
> Update 2026-09-27: FR-5 artifact storage decided (R2 prod + MinIO dev).

## 1. Overview

Digitize UPV student-organization member intake. Students upload their
UP Form 5 (PDF); the portal extracts 6 roster fields in-browser, the
student verifies/corrects and attaches photo + signature under RA 10173
consent, then receives a reference ID. Admins later export a deduplicated
roster (latest submission per student). Uploaded artifacts (Form 5, photo,
signature) persist in S3-compatible storage; the DB stores keys only.

**Why in-browser parsing:** RA 10173 — field extraction runs on-device.
Storing full Form 5 PDFs (FR-5) keeps sensitive blocks server-side, so
encryption, gating, and retention below are mandatory, and the FR-2
consent text must be reworded before production.

## 2. Users

| Segment                | Who                            | Needs                                             | Pain points (prototype evidence)                                                          |
| ---------------------- | ------------------------------ | ------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Registrants (primary)  | UPV students with a Form 5 PDF | Fast upload, pre-filled form, one confirmation ID | Re-typing roster data; typo re-submissions (seed row `DELA CRUZ, Juan Migel` vs `Miguel`) |
| Org admins (secondary) | Roster managers                | Token-gated export console, dedupe, CSV/XLSX      | Manual collapse of duplicate submissions                                                  |

## 3. Scope

**In:** Register view (3 steps), Admin view (login → dashboard → export),
artifact storage (FR-5), all FRs below.
**Out:** Real auth, ID collation (FR-6 planned), payment/financial flows.

## 4. Functional requirements

### FR-1 · Upload & parse (Step 1)

- Dropzone accepts PDF only, max 10 MB. Non-PDF → toast `Only PDF files are accepted.` Oversize → `File exceeds the 10 MB limit.` (interpolated from the enforced constant).
- Parse log (`#parse-log`, `aria-live`) narrates: receipt → text-stream inspection → result.
- Vector path (text-layer glyphs): regex coordinate extraction, `6/6 fields in ~240-360 ms`, chip `TEXT-LAYER PARSE` (green).
- Raster path (scan): Tesseract pass 1/2 (psm 6), mean confidence vs 75% threshold. Below threshold → chip `OCR FALLBACK` (amber) + modal `Low OCR confidence` forcing manual review (button `Review fields manually`).
- Field extraction still discards financial/address/guardian blocks from the
  preview; the stored PDF (FR-5) is the only copy that retains them.

Acceptance: both demo buttons (`Demo: digital`, `Demo: scanned`) reach Step 2 with 6 fields filled and correct chip/modal.

### FR-2 · Review & correct (Step 2)

Split screen: Document Preview (watermarked `UNIVERSITY OF THE PHILIPPINES VISAYAS`, highlighted `.hl` spans per field) | Review & Correct form.

| Field          | Rule (prototype `RULES`)           | Error message                                      |
| -------------- | ---------------------------------- | -------------------------------------------------- |
| student_number | `^20\d{2}-\d{5}$`                  | `Must match format 20YY-XXXXX (e.g., 2024-01234).` |
| full_name      | non-empty                          | `Please enter your full legal name.`               |
| degree_program | non-empty (datalist of 6 programs) | `Please enter your degree program.`                |
| college        | ∈ SBM/CAS/CFOS/SOT                 | `Select your college unit.`                        |
| year_level     | ∈ 1-6                              | `Year level must be between 1 and 6.`              |
| up_mail        | `*@up.edu.ph`                      | `Must be a valid @up.edu.ph address.`              |

- Live validation: green/red borders + per-field source note (`text-layer extraction` vs `OCR (low confidence — please verify)`).
- Attachments: photo (2×2/ID) + signature (white-paper scan), JPG/PNG max 2 MB each, RAM-only preview. Wrong type → toast; oversize → toast.
- Consent checkbox (RA 10173, roster-management scope) — required.
  Production reword must cover server-side artifact retention (FR-5).
- Submit enabled only when: all 6 valid + both attachments + consent. `Start over` resets to Step 1.

### FR-3 · Submit & acknowledge (Step 3)

- Simulated `POST /api/register`: atomic response = acknowledgement + reference ID only (`REG-YYYY-NNNNN`). No stored records ever returned.
- Ack card: ✅, ref ID in dashed box, `Register another member` resets flow.
- FR-2.4: all volatile data incl. attachment data-URLs released after submit (footer + script confirm).
- Production: submit persists artifacts per FR-5, then releases volatile copies.

Acceptance: submit writes one row to roster (visible in Admin in real time), ref ID format correct, uploaders cleared.

### FR-4 · Admin export console

- Token gate (FR-4.1): any non-empty demo token signs in; sign-out clears.
- Stats: raw submissions, unique students, duplicate rows collapsed.
- Dedupe (FR-4.3): `ROW_NUMBER() OVER (PARTITION BY student_number ORDER BY submitted_at DESC) = 1` — green `exported` rows vs red `collapsed` rows, chip `DEDUP: LATEST PER STUDENT`.
- Export CSV: header `id,student_number,full_name,degree_program,college,year_level,up_mail,submitted_at`, quoted, `\r\n`, filename `upv_roster_deduplicated.csv`, toast with row count. Export XLSX: simulated (production streams same result via DuckDB `COPY … FORMAT XLSX`).
- Roster export stays metadata-only; raw files are viewed (never bulk-exported) through the gated file viewer.
- Export scope: every deduped row is exported, including ones whose uploads never completed (`status = pending`) — they are visible in the admin console and rejected at FR-6 render, rather than silently dropped from the roster.
- Seed data: 6 rows incl. deliberate duplicates (typo re-submission + genuine re-submission) to demo the window function.

### FR-5 · Artifact storage (decided 2026-09-27, revised 2026-09-28)

S3 holds bytes, DB holds pointers. **Engine: Garage** (self-hosted,
S3-compatible) for both dev and prod — one stack, one set of semantics,
no cloud account. MinIO was dropped: its community edition was archived
(Feb–Apr 2026) and its Docker Hub images removed (Sep 2026), so it can
no longer be a foundation for a portal holding student data. The backend
speaks plain S3, so any other compatible provider remains a pure env flip:

```bash
# dev (from host) / prod (from the server) — same shape
S3_ENDPOINT=http://localhost:9100   S3_BUCKET=org-roster-dev   S3_REGION=garage
```

- Key layout: `kind/student_number/ref_kind.ext` (e.g.
  `form5/2024-01234/REG-2026-10001_form5.pdf`). The per-student prefix
  makes RA 10173 erasure a one-prefix delete; the ref segment keeps a
  re-submission from overwriting the previous submission's object,
  which would leave the older `files` row pointing at a different sha256.
- DB stores the object **key**, never a full URL. Serving mints
  presigned URLs (5–15 min expiry) behind the token gate — the bucket
  stays private.
- Upload order: S3 first, then DB row with key + `sha256`. The client
  never proxies bytes through the API: `POST /api/register` mints the
  ref, a second call returns presigned PUTs, the browser uploads
  directly, and a `complete` call records the rows. A sweeper clears
  orphans (objects belonging to registrations still `pending` after 7
  days). Never a DB row pointing at nothing.
- `sha256` stored per artifact; ID generation (FR-6) verifies before
  rendering so corrupt/tampered files never reach print.
- Lifecycle: staging uploads expire after 7 days; closed windows
  transition to cheaper class.

Acceptance: one registration yields 3 `files` rows; presigned view works
gated; re-pointing env from MinIO to R2 needs no code change.

## 5. Data model

`registrations`: `id` (auto) · `student_number` (dedup key) ·
`full_name` · `degree_program` · `college` · `year_level` (int 1-6) ·
`up_mail` · `submitted_at` (UTC ISO) · `ref` (`REG-YYYY-NNNNN`) ·
`status` (`pending` | `complete`, amended 2026-09-28 — `pending` until the
three artifact uploads finish, so an abandoned registration is visible
to admins rather than silently "successful").

`files`: `id` · `registration_id → registrations` ·
`kind` (form5|photo|signature|id_doc) · `storage_key` · `mime` ·
`bytes` · `sha256` · `created_at`.

## 6. Non-functional requirements

- Privacy (RA 10173): parsing + previews 100% client-side; attachments never touch disk/server in demo. Production: private bucket, SSE at rest, TLS, presigned-only serving, consent reword, retention + erasure path.
- Performance budgets: vector parse ≤ 400 ms; simulated WAL commit ≤ 35 ms.
- Upload limits: PDF 10 MB, images 5 MB each (~20 MB/member ceiling).
- Accessibility: dropzone keyboard-operable, `aria-live` parse log, labelled inputs.
- Theme divergence (known): prototype uses maroon `#7B1113`/gold `#E8C766`; production theme is pine-teal `#004A36`/wine `#7B1113`/amber `#FFB81C` (WCAG-fixed, see `frontend/src/css/`). Re-skin on implementation.

## 7. Open questions for production

1. Backend: real API + DB (SQLite `registrations.db` per prototype SQL block, or Postgres)? Who hosts?
2. Auth: real admin token scheme (FR-4.1 demo accepts anything)?
3. OCR: client Tesseract.js vs server OCR service? Keep 75% threshold?
4. ~~Storage~~ Resolved (FR-5: self-hosted Garage, S3-compatible, key-pointer schema).
5. Reference IDs: server-sequenced vs random? Collision handling?
6. XLSX: real generator lib (prototype only simulates)?
7. Programs list: authoritative degree-program source vs 6-item datalist?
8. FR-6 ID collation: PVC CR80 cards or PDF sheets? Existing card design?
