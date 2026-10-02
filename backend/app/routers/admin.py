"""Admin export console (PRD FR-4). Every route is behind the token gate.

The router-level `dependencies` applies `require_admin` to each path
here, so no handler can forget it (FR-4.1).
"""

import csv
import io
from contextlib import closing

from fastapi import APIRouter, Depends, HTTPException, Response, status

from .. import config, db, dedupe, storage
from ..deps import require_admin

router = APIRouter(
    prefix="/api/admin",
    tags=["admin"],
    dependencies=[Depends(require_admin)],
)

CSV_HEADER = [
    "id",
    "student_number",
    "full_name",
    "degree_program",
    "college",
    "year_level",
    "up_mail",
    "submitted_at",
]

# FR-4 seed data, verbatim from the prototype. Deliberate duplicates
# (typo re-submission + genuine re-submission) demo the dedupe window.
SEED_ROWS = [
    ("2024-01234", "DELA CRUZ, Juan Miguel, S.", "BS Computer Science", "CAS", 3, "jmdelacruz@up.edu.ph", "2027-01-05T02:11:00Z", "REG-2027-44102"),
    ("2024-01234", "DELA CRUZ, Juan Migel, S.", "BS Computer Science", "CAS", 3, "jmdelacruz@up.edu.ph", "2027-01-05T06:47:00Z", "REG-2027-51277"),
    ("2023-08765", "REYES, Maria Isabel", "BA Communication and Media Studies", "CAS", 2, "mireyes@up.edu.ph", "2027-01-06T09:03:00Z", "REG-2027-53018"),
    ("2022-00341", "SANTOS, Paolo Ramirez", "BS Accountancy", "SBM", 4, "prsantos@up.edu.ph", "2027-01-06T11:22:00Z", "REG-2027-53466"),
    ("2025-00918", "LIM, Andrea Nicole, T.", "BS Fisheries", "CFOS", 1, "anlim@up.edu.ph", "2027-01-07T01:15:00Z", "REG-2027-55109"),
    ("2023-08765", "REYES, Maria Isabel", "BA Communication and Media Studies", "CAS", 2, "mireyes@up.edu.ph", "2027-01-07T03:40:00Z", "REG-2027-55821"),
]


def _load_roster(conn) -> list:
    """All registrations, newest-first per student, with file counts."""
    return conn.execute(
        "SELECT r.*, "
        "(SELECT COUNT(*) FROM files f WHERE f.registration_id = r.id) AS files_count "
        f"FROM registrations r ORDER BY {dedupe.ROSTER_ORDER}"
    ).fetchall()


@router.get("/stats")
def stats() -> dict[str, int]:
    """Headline counters (FR-4.2)."""
    with closing(db.connect()) as conn:
        rows = conn.execute(
            f"SELECT student_number, status FROM registrations ORDER BY {dedupe.ROSTER_ORDER}"
        ).fetchall()
    return dedupe.compute_stats(rows)


@router.get("/roster")
def roster() -> dict:
    """Roster rows with `exported` / `duplicates` badges and file counts."""
    with closing(db.connect()) as conn:
        rows = _load_roster(conn)
    return {"rows": dedupe.annotate(rows)}


@router.get("/export.csv")
def export_csv() -> Response:
    """Dedupe-latest CSV (FR-4.4).

    Returns a plain `Response` with a hand-set `Content-Disposition`,
    which is what turns the response into a browser download. All fields
    are quoted, line endings are CRLF, and every deduped row is included
    (F.3=i: pending rows are surfaced here and caught at FR-6 render).
    """
    with closing(db.connect()) as conn:
        rows = conn.execute(f"SELECT * FROM registrations ORDER BY {dedupe.ROSTER_ORDER}").fetchall()
    winners = dedupe.latest_per_student(rows)

    buffer = io.StringIO()
    writer = csv.writer(buffer, quoting=csv.QUOTE_ALL, lineterminator="\r\n")
    writer.writerow(CSV_HEADER)
    for row in winners:
        writer.writerow([row[column] for column in CSV_HEADER])

    return Response(
        content=buffer.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="upv_roster_deduplicated.csv"'},
    )


@router.get("/files/{file_id}/url")
def file_url(file_id: int) -> dict:
    """Gated presigned GET for the file viewer (FR-5)."""
    with closing(db.connect()) as conn:
        file = conn.execute("SELECT * FROM files WHERE id = ?", (file_id,)).fetchone()
    if file is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unknown file id.")
    client = storage.get_client()
    return {
        "url": storage.presign_get(client, config.S3_BUCKET, file["storage_key"], config.PRESIGN_GET_EXPIRES),
        "expires_in": config.PRESIGN_GET_EXPIRES,
        "kind": file["kind"],
        "sha256": file["sha256"],
    }


@router.post("/seed", status_code=status.HTTP_201_CREATED)
def seed() -> dict:
    """Load the 6 prototype rows. Idempotent — 409 if already seeded."""
    with closing(db.connect()) as conn:
        existing = conn.execute(
            "SELECT COUNT(*) AS n FROM registrations WHERE ref LIKE 'REG-2027-%'"
        ).fetchone()["n"]
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Seed data already present.",
            )
        conn.execute("BEGIN IMMEDIATE")
        try:
            for row in SEED_ROWS:
                conn.execute(
                    "INSERT INTO registrations "
                    "(student_number, full_name, degree_program, college, year_level, "
                    " up_mail, submitted_at, ref, status) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'complete')",
                    row,
                )
            # db.connect() runs in autocommit mode, so an explicit BEGIN only
            # opens a transaction. Without this COMMIT the connection close in
            # the `with` block discards all six rows and the 201 is a lie.
            conn.commit()
        except Exception:
            conn.execute("ROLLBACK")
            raise
    return {"seeded": len(SEED_ROWS)}
