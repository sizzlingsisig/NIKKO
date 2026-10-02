/**
 * Deduplication, ordering and CSV serialisation for the admin roster.
 *
 * The rule is "latest `submitted_at` per `student_number` wins", mirroring
 * `ROW_NUMBER() OVER (PARTITION BY student_number ORDER BY submitted_at DESC) = 1`
 * in `backend/app/dedupe.py`. Every function here is pure.
 */

import type {
  AnnotatedRosterRow,
  RosterRow,
  RosterStats
} from "./registration";

export const CSV_HEADER = [
  "id",
  "student_number",
  "full_name",
  "degree_program",
  "college",
  "year_level",
  "up_mail",
  "submitted_at"
] as const;

export const CSV_FILENAME = "upv_roster_deduplicated.csv";

/** One winner per student number — the set that gets exported. */
export const latestPerStudent = (
  rows: readonly RosterRow[]
): readonly RosterRow[] => {
  const winners = new Map<string, RosterRow>();
  for (const row of rows) {
    const incumbent = winners.get(row.student_number);
    if (!incumbent || row.submitted_at > incumbent.submitted_at) {
      winners.set(row.student_number, row);
    }
  }
  return [...winners.values()];
};

export const annotateRoster = (
  rows: readonly RosterRow[]
): readonly AnnotatedRosterRow[] => {
  const winnerIds = new Set(latestPerStudent(rows).map(row => row.id));
  return rows.map(row => ({ ...row, is_latest: winnerIds.has(row.id) }));
};

/** Student number ascending, then newest submission first within a student. */
export const sortRoster = <T extends RosterRow>(rows: readonly T[]): T[] =>
  [...rows].sort(
    (a, b) =>
      a.student_number.localeCompare(b.student_number) ||
      b.submitted_at.localeCompare(a.submitted_at)
  );

export const computeStats = (rows: readonly RosterRow[]): RosterStats => {
  const unique = latestPerStudent(rows).length;
  return { raw: rows.length, unique, collapsed: rows.length - unique };
};

export const escapeCsvCell = (value: unknown): string =>
  `"${String(value).replace(/"/g, '""')}"`;

/**
 * Deduplicated export: one row per student, every cell quoted, CRLF line
 * endings — byte-compatible with `GET /api/admin/export.csv`.
 */
export const buildRosterCsv = (rows: readonly RosterRow[]): string => {
  const winners = sortRoster(latestPerStudent(rows));
  return [CSV_HEADER, ...winners.map(row => CSV_HEADER.map(c => row[c]))]
    .map(line => line.map(escapeCsvCell).join(","))
    .join("\r\n");
};

export const formatBytes = (bytes: number): string => {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${Math.round(bytes / 1024)} KB`;
  // Drop the decimal only when it would be `.0`, so a stated ceiling reads
  // "10 MB" while a real file size keeps its precision ("7.5 MB").
  const mb = bytes / (1024 * 1024);
  return `${Number.isInteger(mb) ? mb : mb.toFixed(1)} MB`;
};
