# Docker Commands

Cheat sheet for the Form5 Portal stack. Run everything from the repo root.

## First time only

```bash
cp .env.example .env
docker compose --profile dev up -d --build
```

`--profile dev` is required — Garage sits behind `profiles: [dev]`, so a plain
`docker compose up` silently skips it and every upload fails later.

## Daily use

```bash
docker compose up -d          # start
docker compose stop           # stop, keep containers
docker compose restart api    # restart one service
docker compose down           # stop and remove containers
docker compose ps             # what is running
docker compose logs -f api    # follow one log
```

## After changing code

Images are snapshots — code edits on the host do nothing until you rebuild.

```bash
docker compose up -d --build api    # backend changes
docker compose up -d --build web    # frontend changes
docker compose up -d --build        # both
```

## Ports

| Service | URL | Notes |
| --- | --- | --- |
| web | http://localhost | the portal |
| api | http://localhost:8000 | OpenAPI at `/docs` |
| garage (S3) | http://localhost:9100 | object storage |
| garage UI | http://localhost:3902 | optional web console |

Health check:

```bash
curl http://localhost:8000/health        # {"status":"ok"}
```

## Seeding test data

```bash
# ADMIN_TOKEN defaults to "change-me" in .env — override it for anything real
curl -X POST http://localhost:8000/api/admin/seed \
  -H "Authorization: Bearer change-me"
```

Adds 6 rows containing 2 deliberate duplicates, so the dedupe view has something
to collapse. Returns 409 if seed rows are already present.

## Handy one-offs

```bash
docker compose exec api .venv/bin/python -c "..."   # python inside the container
docker compose logs --tail=50 web                   # last 50 lines, no follow
docker compose down -v                              # DESTROYS the database + object store
```

`down -v` deletes the `form5-data`, `garage-meta` and `garage-data` volumes. There
is no undo — re-seed afterwards to get back to a known state.

## Troubleshooting

**`404` on `/api/register` or `/api/admin/*`, or openapi shows one path**
The image is older than the source. Confirm with `docker compose ps` (look at the
`CREATED` column) and rebuild: `docker compose up -d --build api`.

**`POST /api/admin/seed` returns `201 {"seeded":6}` but `/stats` stays at zero**
Same cause — a stale image. Rebuild `api`.

**Connection errors mentioning `garage:3900`**
Garage is not running. It needs the dev profile: `docker compose --profile dev up -d garage`.

**`409` on seed but you want to start clean**
The seed rows are still there. Either leave them, or `docker compose down -v` and
rebuild the stack from scratch.

## Known issues

- **Presigned upload URLs are not browser-reachable.** The API signs PUT URLs with
  the compose-internal hostname `http://garage:3900`, which does not resolve on the
  host and cannot be rewritten without invalidating the signature (`host` is a signed
  header). The portal currently uses local mock data, so this is hidden — it will
  block the real upload flow when the API is wired up.
- **Frontend image uses `npm ci`, the host uses pnpm.** The lockfiles are separate;
  a dependency added on the host will not be picked up by `docker compose up -d --build web`.