"""Reference ID minting (PRD FR-3: sequential `REG-YYYY-NNNNN`).

Sequencing is per calendar year: each year restarts at 10000. The
generation and the INSERT are one function so the UNIQUE retry can wrap
both and never hand the same ref to two students.
"""

import sqlite3
from datetime import datetime, timezone

FIRST_SEQUENCE = 10_000
MAX_REF_ATTEMPTS = 5

INSERT_REGISTRATION = """
INSERT INTO registrations (
    student_number, full_name, degree_program, college,
    year_level, up_mail, submitted_at, ref, status
) VALUES (
    :student_number, :full_name, :degree_program, :college,
    :year_level, :up_mail, :submitted_at, :ref, 'pending'
)
"""


def utc_now_iso() -> str:
    """UTC timestamp as the app stores it: second precision, `Z` suffix."""
    stamp = datetime.now(timezone.utc).replace(microsecond=0)
    return stamp.isoformat().replace("+00:00", "Z")


def next_sequence(conn: sqlite3.Connection, year: int) -> int:
    """Highest sequence issued this year, plus one."""
    row = conn.execute(
        "SELECT MAX(CAST(SUBSTR(ref, 10) AS INTEGER)) AS max_seq "
        "FROM registrations WHERE SUBSTR(ref, 1, 4) = ?",
        (str(year),),
    ).fetchone()
    return max(row["max_seq"] or 0, FIRST_SEQUENCE - 1) + 1


def insert_registration(conn: sqlite3.Connection, values: dict) -> str:
    """Insert a pending registration and return its ref.

    Retries on the UNIQUE conflict that two requests racing at a year
    rollover would produce; the last attempt re-raises.
    """
    year = datetime.now(timezone.utc).year
    for attempt in range(MAX_REF_ATTEMPTS):
        ref = f"REG-{year}-{next_sequence(conn, year):05d}"
        try:
            conn.execute(INSERT_REGISTRATION, {**values, "ref": ref, "submitted_at": utc_now_iso()})
            return ref
        except sqlite3.IntegrityError:
            if attempt == MAX_REF_ATTEMPTS - 1:
                raise
    raise RuntimeError("unreachable: ref generation loop always returns or raises")
