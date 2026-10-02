"""Environment-driven configuration.

Every knob the app reads lives here so the same code runs against local
Garage and a self-hosted deployment (PRD FR-5: env-only switch, no code
change).
"""

import os
from pathlib import Path

# Admin token gate (FR-4.1). The default keeps host-side dev frictionless.
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "change-me")

# SQLite location. Unset (e.g. host-side `uvicorn`) falls back to a file
# next to the backend package so dev never needs the compose volume.
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    f"sqlite:///{Path(__file__).resolve().parent.parent / 'registrations.db'}",
)

# S3-compatible object storage (FR-5). Garage in dev and prod; the same
# values work for MinIO or R2 if the deployment ever changes.
S3_ENDPOINT = os.environ.get("S3_ENDPOINT", "http://localhost:9100")
S3_REGION = os.environ.get("S3_REGION", "garage")
S3_BUCKET = os.environ.get("S3_BUCKET", "org-roster-dev")
S3_ACCESS_KEY_ID = os.environ.get("S3_ACCESS_KEY_ID", "form5portalaccess")
S3_SECRET_ACCESS_KEY = os.environ.get("S3_SECRET_ACCESS_KEY", "form5portaldevsecret")

# Presigned URL lifetimes (FR-5 serving window).
PRESIGN_PUT_EXPIRES = int(os.environ.get("PRESIGN_PUT_EXPIRES", "900"))
PRESIGN_GET_EXPIRES = int(os.environ.get("PRESIGN_GET_EXPIRES", "3600"))

# Per-artifact size ceilings (PRD §6): PDF 10 MB, images 5 MB each.
#
# Expressed in megabytes so the same knob is readable in `.env`. These MUST stay
# in lockstep with `MAX_PDF_BYTES` / `MAX_IMAGE_BYTES` in
# `frontend/src/domain/validation.ts` — the browser validates first, so a
# frontend-only bump would let a student upload a file this API answers 413 to.
PDF_MAX_MB = int(os.environ.get("PDF_MAX_MB", "10"))
IMAGE_MAX_MB = int(os.environ.get("IMAGE_MAX_MB", "5"))

MAX_ARTIFACT_BYTES = {
    "form5": PDF_MAX_MB * 1024 * 1024,
    "photo": IMAGE_MAX_MB * 1024 * 1024,
    "signature": IMAGE_MAX_MB * 1024 * 1024,
}

REQUIRED_ARTIFACT_KINDS = ("form5", "photo", "signature")

# Browser origins allowed to call the API (frontend dev server + compose web).
CORS_ORIGINS = [
    origin.strip()
    for origin in os.environ.get(
        "CORS_ORIGINS",
        "http://localhost:8080,http://localhost:5173,http://localhost",
    ).split(",")
    if origin.strip()
]


def sqlite_path() -> Path:
    """Filesystem path behind a SQLite DATABASE_URL."""
    return Path(DATABASE_URL.removeprefix("sqlite:///"))
