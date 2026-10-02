"""SQLite access layer: schema definition plus connection setup.

The schema lives here and nowhere else so the table shape has a single
home (PRD §5, amended with the `status` column that marks whether the
three artifact uploads finished).
"""

import sqlite3
from contextlib import closing
from pathlib import Path

from . import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS registrations (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    student_number TEXT    NOT NULL,
    full_name      TEXT    NOT NULL,
    degree_program TEXT    NOT NULL,
    college        TEXT    NOT NULL,
    year_level     INTEGER NOT NULL CHECK (year_level BETWEEN 1 AND 6),
    up_mail        TEXT    NOT NULL,
    submitted_at   TEXT    NOT NULL,
    ref            TEXT    NOT NULL UNIQUE,
    status         TEXT    NOT NULL DEFAULT 'pending'
                   CHECK (status IN ('pending', 'complete'))
);

CREATE INDEX IF NOT EXISTS idx_registrations_student
    ON registrations (student_number, submitted_at DESC, id DESC);
CREATE INDEX IF NOT EXISTS idx_registrations_status
    ON registrations (status);

CREATE TABLE IF NOT EXISTS files (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    registration_id INTEGER NOT NULL REFERENCES registrations (id) ON DELETE CASCADE,
    kind            TEXT    NOT NULL
                    CHECK (kind IN ('form5', 'photo', 'signature', 'id_doc')),
    storage_key     TEXT    NOT NULL,
    mime            TEXT    NOT NULL,
    bytes           INTEGER NOT NULL,
    sha256          TEXT    NOT NULL,
    created_at      TEXT    NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_files_registration
    ON files (registration_id);
"""


def connect(path: Path | str | None = None) -> sqlite3.Connection:
    """Open a tuned connection (WAL + foreign keys) to the SQLite file.

    Autocommit mode keeps transaction boundaries explicit in the routers
    that need them, so a failed insert can never leave half a write.
    """
    target = Path(path) if path is not None else config.sqlite_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(target, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    """Create tables and indexes if absent. Idempotent, so it runs on boot."""
    with closing(connect()) as conn:
        conn.executescript(SCHEMA)
