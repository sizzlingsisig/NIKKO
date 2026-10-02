"""Student-facing flow (PRD FR-3 + FR-5): register → presign → complete.

The three-step handshake keeps bytes off the server (F.1b): the client
gets a ref, asks for presigned PUTs, uploads straight to object storage,
then reports what it uploaded. The server never proxies file content.
"""

import sqlite3
from contextlib import closing

from fastapi import APIRouter, HTTPException, status

from .. import config, db, refs, storage
from ..schemas import ArtifactClaim, RegistrationIn

router = APIRouter(prefix="/api/register", tags=["register"])

# Canonical object extensions per artifact kind. Fixed so the key the
# server records at `/complete` is the same key it presigned earlier.
KIND_EXT = {"form5": "pdf", "photo": "png", "signature": "png"}


def artifact_key(kind: str, student_number: str, ref: str) -> str:
    """Object key: `kind/student_number/ref_kind.ext`.

    The ref segment makes a re-submission land on a *new* key instead of
    overwriting the previous submission's artifact, which would leave the
    older `files` row pointing at a different sha256. The per-student
    prefix still makes RA 10173 erasure a single-prefix delete.
    """
    return f"{kind}/{student_number}/{ref}_{kind}.{KIND_EXT[kind]}"


def _get_registration(conn: sqlite3.Connection, ref: str) -> sqlite3.Row:
    row = conn.execute("SELECT * FROM registrations WHERE ref = ?", (ref,)).fetchone()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unknown ref {ref}.")
    return row


@router.post("", status_code=status.HTTP_201_CREATED)
def register(payload: RegistrationIn) -> dict[str, str]:
    """FR-3: acknowledge and hand back a ref. Returns no stored record."""
    values = payload.model_dump(exclude={"consent"})
    with closing(db.connect()) as conn:
        ref = refs.insert_registration(conn, values)
    return {"ref": ref}


@router.post("/{ref}/artifacts")
def presign_artifacts(ref: str) -> dict:
    """FR-5: mint a presigned PUT URL per required artifact kind."""
    with closing(db.connect()) as conn:
        registration = _get_registration(conn, ref)
    if registration["status"] == "complete":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This registration is already complete.",
        )

    client = storage.get_client()
    uploads = {}
    for kind in config.REQUIRED_ARTIFACT_KINDS:
        key = artifact_key(kind, registration["student_number"], ref)
        uploads[kind] = {
            "key": key,
            "url": storage.presign_put(client, config.S3_BUCKET, key, config.PRESIGN_PUT_EXPIRES),
            "expires_in": config.PRESIGN_PUT_EXPIRES,
            "max_bytes": config.MAX_ARTIFACT_BYTES[kind],
        }
    return {"ref": ref, "uploads": uploads}


@router.post("/{ref}/complete")
def complete(ref: str, claims: list[ArtifactClaim]) -> dict:
    """FR-5: verify the uploaded objects, then record them in one txn.

    Size and existence are checked against object storage (the client
    only *claims* sha256 — FR-6 re-verifies before any render), so the
    DB can never end up pointing at nothing.
    """
    with closing(db.connect()) as conn:
        registration = _get_registration(conn, ref)
    if registration["status"] == "complete":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This registration is already complete.",
        )

    claim_by_kind = {claim.kind: claim for claim in claims}
    if set(claim_by_kind) != set(config.REQUIRED_ARTIFACT_KINDS):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Complete requires exactly these kinds: {', '.join(config.REQUIRED_ARTIFACT_KINDS)}.",
        )

    client = storage.get_client()
    student_number = registration["student_number"]
    sizes: dict[str, int] = {}
    for kind in config.REQUIRED_ARTIFACT_KINDS:
        key = artifact_key(kind, student_number, ref)
        size = storage.head_size(client, config.S3_BUCKET, key)
        if size is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"No uploaded object found for '{kind}'.",
            )
        # A 0-byte object is a truncated or failed upload, not a valid
        # artifact: the ceiling check would pass it. Reject it like a
        # missing object and delete the junk so it cannot be mistaken
        # for a real upload later.
        if size == 0:
            storage.delete_object(client, config.S3_BUCKET, key)
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"'{kind}' is empty (0 bytes); re-upload the file.",
            )
        limit = config.MAX_ARTIFACT_BYTES[kind]
        if size > limit:
            storage.delete_object(client, config.S3_BUCKET, key)
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"'{kind}' is {size} bytes; limit is {limit}.",
            )
        sizes[kind] = size

    created = refs.utc_now_iso()
    rows = [
        (kind, claim_by_kind[kind].sha256, claim_by_kind[kind].mime, sizes[kind], created)
        for kind in config.REQUIRED_ARTIFACT_KINDS
    ]
    with closing(db.connect()) as conn:
        conn.execute("BEGIN IMMEDIATE")
        try:
            file_ids = _write_files_and_complete(conn, registration["id"], student_number, ref, rows)
            # db.connect() runs in autocommit mode, so this explicit BEGIN
            # needs an explicit commit — without it closing() would discard
            # the open transaction and silently roll back every insert.
            conn.commit()
        except Exception:
            conn.execute("ROLLBACK")
            raise
    return {
        "ref": ref,
        "status": "complete",
        "files": file_ids,
    }


def _write_files_and_complete(
    conn: sqlite3.Connection,
    registration_id: int,
    student_number: str,
    ref: str,
    rows: list[tuple[str, str, str, int, str]],
) -> list[dict]:
    """Insert the three `files` rows and flip `status` atomically."""
    file_ids: list[dict] = []
    for kind, sha256, mime, size, created in rows:
        key = artifact_key(kind, student_number, ref)
        cursor = conn.execute(
            "INSERT INTO files (registration_id, kind, storage_key, mime, bytes, sha256, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (registration_id, kind, key, mime, size, sha256, created),
        )
        file_ids.append({"id": cursor.lastrowid, "kind": kind})
    conn.execute("UPDATE registrations SET status = 'complete' WHERE id = ?", (registration_id,))
    return file_ids
