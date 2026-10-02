"""Roster deduplication (PRD FR-4.3: latest submission per student).

Pure functions over already-sorted rows: the router owns the query and
this module owns the arithmetic, so the rule stays testable on its own.

The tiebreak is `submitted_at DESC, id DESC` — the same ordering the SQL
window in the prototype used, with `id` breaking exact-timestamp ties.
"""

import sqlite3
from collections import Counter
from collections.abc import Sequence

Row = sqlite3.Row

# Shared newest-first ordering for dedupe and the roster listing.
ROSTER_ORDER = "student_number ASC, submitted_at DESC, id DESC"


def latest_per_student(rows: Sequence[Row]) -> list[Row]:
    """The first row per student in newest-first order (the exported ones)."""
    seen: set[str] = set()
    winners: list[Row] = []
    for row in rows:
        student_number = row["student_number"]
        if student_number in seen:
            continue
        seen.add(student_number)
        winners.append(row)
    return winners


def annotate(rows: Sequence[Row]) -> list[dict]:
    """Roster rows plus the `exported` / `duplicates` badges the UI shows."""
    submissions_per_student = Counter(row["student_number"] for row in rows)
    exported_ids = {winner["id"] for winner in latest_per_student(rows)}
    return [
        {
            **dict(row),
            "exported": row["id"] in exported_ids,
            "duplicates": submissions_per_student[row["student_number"]] - 1,
        }
        for row in rows
    ]


def compute_stats(rows: Sequence[Row]) -> dict[str, int]:
    """Headline counters (PRD FR-4.2) derived from the same dedupe rule."""
    winners = latest_per_student(rows)
    return {
        "raw": len(rows),
        "unique_students": len(winners),
        "duplicates": len(rows) - len(winners),
        "pending": sum(1 for row in rows if row["status"] == "pending"),
    }
