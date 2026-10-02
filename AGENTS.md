# AGENTS.md

Form5 Portal (**NIKKO**): UPV org member intake — students upload a UP Form 5
PDF, roster fields are extracted in-browser, admins dedupe and export. Current
build is a labeled **prototype/simulation** (PRODUCT.md: never imply live capability).

## Layout

- `frontend/` — Quasar (Vue 3 + Vite + TS) SPA; pages `src/pages/register.vue`, `admin.vue`
- `backend/` — FastAPI in `backend/app/` (`routers/{register,admin,health}.py`), SQLite + Garage/S3 (boto3)
- `bruno/` — Bruno API collection (GUI app `bruno`; no headless `bru` CLI installed)
- Source docs: `COMMANDS.md` (docker ops + troubleshooting), `PRD.md` (requirements),
  `PRODUCT.md` (constraints/brand), `DESIGN.md` (design system — read before UI work)
- Decision records: `docs/adr/` (accepted decisions — scope, schema, auth) and
  `docs/GLOSSARY.md` (binding domain vocabulary). Consult before changing
  scope, schema, or terminology; PRD/PRODUCT defer to the ADRs where they conflict.

## Commands (run from repo root unless noted)

First time:

```bash
cp .env.example .env
docker compose --profile dev up -d --build
```

`--profile dev` is REQUIRED — Garage sits behind it; plain `up` silently skips
Garage and every upload fails later.

After code edits: containers are snapshots — `docker compose up -d --build api`
or `--build web`. Full cheat sheet: `COMMANDS.md`.

Host-side dev (no compose):

- Frontend (`cd frontend`): use **npm** (pnpm is NOT installed; lockfile is `package-lock.json`,
  despite `frontend/README.md` suggesting pnpm) — `npm run dev` (port 9000),
  `npm run lint:check` → `npm run typecheck` (verify order), `npm run lint` fixes.
- Backend (`cd backend`, `uv` available): `uv run uvicorn app.main:app` — defaults
  work host-side (SQLite file beside app, Garage at `localhost:9100`).

**No automated tests and no CI exist.** Verification = lint + typecheck (frontend)
and boot smoke (`curl localhost:8000/health`, OpenAPI at `/docs`). API calls via
the Bruno collection; seed with `POST /api/admin/seed` + `Authorization: Bearer change-me`.

## Gotchas an agent would miss

- Upload limits are defined in TWO places: `.env` `PDF_MAX_MB`/`IMAGE_MAX_MB` must match
  `MAX_PDF_BYTES`/`MAX_IMAGE_BYTES` in `frontend/src/domain/validation.ts`, or the
  browser accepts files the API answers 413 to.
- Frontend makes **no network requests** — data flows through `src/domain/mockData.ts`.
  The `Simulation` badge must stay honest (PRODUCT.md principle 4).
- Presigned PUT URLs are signed with compose-internal `http://garage:3900` → not
  reachable from the browser. Known issue; do NOT "fix" by rewriting the endpoint
  (`host` is a signed header — rewriting invalidates the signature).
- `.env` is NOT actually gitignored (root `.gitignore` omits it, though `.env.example`
  claims otherwise) — never `git add .env`.
- Colocated `src/pages/**/components/` are import-only: `quasar.config.ts` excludes
  them from filename-based routing. New routes = files directly under `src/pages/`.
- `docker compose down -v` destroys the DB + object-store volumes (no undo; re-seed after).
  404s on `/api/*` or seed-OK-but-stats-zero = stale image → rebuild `api` (see COMMANDS.md).
- Root `.gitignore` excludes agent artifacts: `docs/superpowers/`, `.opencode/`,
  `.impeccable/`, `.agents/`, `.superpowers/`, `.tmp/` — local only, don't commit.

## Conventions

- Commits: conventional with scope — `feat(register):`, `fix:`, `docs:` (per git log).
- Domain terms: "Form 5", reference ID `REG-YYYY-NNNNN`, dedupe = latest submission
  per student, colleges SBM/CAS/CFOS/SOT, `@up.edu.ph` only.
- Design: `DESIGN.md` is WCAG-fixed (AA floor, measured contrast); fonts are
  Plus Jakarta Sans + JetBrains Mono (Roboto intentionally absent); material-icons
  webfont must stay; ripple intentionally off; UP Visayas seal is binding.
