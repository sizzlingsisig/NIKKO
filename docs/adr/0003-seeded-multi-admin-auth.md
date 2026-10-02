# ADR-0003: Admin auth — seeded multi-admin accounts with sessions

**Status:** Accepted — 2026-10-02 (grilled interview, user decision)

## Context

Pass 1 requires "real admin auth" (ADR-0001). The user chose **multi-admin
accounts** over single-password options — the org has multiple officers.
At 3–5 hrs/week, provisioning must not become a user-management project.

## Decision

- Multiple named admin accounts; password login → signed httpOnly session
  cookie with expiry; passwords hashed at rest.
- **Seed-only provisioning:** accounts are created via a CLI command or env
  seed. No public signup, no invite codes, no self-registration UI. No
  admin-facing account management in pass 1.
- **SQLite stays** (PRD §7 DB question closed for pass 1): `admins` +
  `sessions` tables live in the existing database. Postgres is revisited
  only when hosting is decided (currently deferred — localhost).
- The demo bearer token (`ADMIN_TOKEN`) retires once login lands; it may
  remain as the bootstrap/seed secret.

## Consequences

- Rough scope: login route + session middleware + logout + seed command
  (~2–3 days of budget).
- Admin creation/rotation = manual CLI ops — acceptable for a single org.
- **Decided 2026-10-02:** sessions are **12h sliding** (renew on activity,
  expire after 12h idle). Password reset = CLI. Admin provisioning = seed
  command only (see Decision).
- Still parked: audit logging (deferred), all admins equal (no roles).
