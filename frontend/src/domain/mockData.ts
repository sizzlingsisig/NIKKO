/**
 * Local mock data and the scripted parse narration.
 *
 * This module is the *simulation* layer the PRD calls for: no network, no
 * pdfjs-dist, no tesseract.js. An accepted PDF replays a timed log script
 * (FR-1) and prefills the six fields, exactly as
 * `form5_portal_prototype.html` does. Swapping this for real parsing later
 * means replacing `buildParseScript` with actual worker output — nothing else
 * changes. `MOCK_RASTER` is the dormant fixture for that OCR pass.
 */

import type { ParsedForm5, RosterRow } from "./registration";
import { OCR_CONFIDENCE_THRESHOLD } from "./validation";

export const MOCK_VECTOR: ParsedForm5 = {
  fileName: "form5_vector_demo.pdf",
  mode: "vector",
  fields: {
    student_number: "2024-01234",
    full_name: "DELA CRUZ, Juan Miguel, Santos",
    degree_program: "BS Computer Science",
    college: "CAS",
    year_level: "3",
    up_mail: "jmdelacruz@up.edu.ph"
  }
};

export const MOCK_RASTER: ParsedForm5 = {
  fileName: "form5_scanned_demo.pdf",
  mode: "raster",
  ocrConfidence: 61,
  fields: {
    student_number: "2023-08765",
    full_name: "REYES, Maria Isabel",
    degree_program: "BA Communication and Media Studies",
    college: "CAS",
    year_level: "2",
    up_mail: "mireyes@up.edu.ph"
  }
};

/** Re-label a demo payload for a file the student actually dropped. */
export const renameSource = (
  parsed: ParsedForm5,
  fileName: string
): ParsedForm5 => ({
  ...parsed,
  fileName
});

export type LogTone = "dim" | "ok" | "warn" | "pending";

export interface LogLine {
  tone: LogTone;
  text: string;
  /** Milliseconds to wait *after* rendering this line. */
  hold: number;
}

/** The narrative the parse log plays, one entry per line. */
export const buildParseScript = (
  parsed: ParsedForm5,
  elapsedMs: number
): readonly LogLine[] => {
  const received: LogLine = {
    tone: "dim",
    text: `Received ${parsed.fileName}. Held in browser RAM only`,
    hold: 0
  };

  if (parsed.mode === "vector") {
    return [
      received,
      {
        tone: "pending",
        text: "pdfjs-dist: inspecting text streams…",
        hold: 500
      },
      { tone: "ok", text: "vector text glyphs detected", hold: 0 },
      {
        tone: "pending",
        text: "regex coordinate extraction: ^20\\d{2}-\\d{5}$ …",
        hold: 450
      },
      {
        tone: "ok",
        text: `extracted 6/6 fields in ${elapsedMs} ms (NFR ≤ 400 ms)`,
        hold: 0
      },
      {
        tone: "dim",
        text: "financial assessment / home address / guardian blocks discarded",
        hold: 350
      }
    ];
  }

  const confidence = parsed.ocrConfidence ?? 0;
  return [
    received,
    {
      tone: "warn",
      text: "no text glyphs found, raster image / scan detected",
      hold: 0
    },
    { tone: "pending", text: "tesseract.js worker: OCR pass 1/2…", hold: 800 },
    {
      tone: "pending",
      text: "tesseract.js worker: OCR pass 2/2 (psm 6)…",
      hold: 800
    },
    {
      tone: "warn",
      text: `OCR mean confidence ${confidence}% < ${OCR_CONFIDENCE_THRESHOLD}% threshold`,
      hold: 0
    },
    { tone: "dim", text: "→ prompting manual review (FR-1.3)", hold: 0 }
  ];
};

/** Randomised but bounded parse duration, matching the prototype's 240–360 ms. */
export const simulateParseDuration = (
  rand: () => number = Math.random
): number => Math.round(240 + rand() * 120);

/**
 * The six seed rows, including the deliberate duplicate pairs the admin
 * console uses to demonstrate collapsing (FR-4.3). Mirrors `SEED_ROWS` in
 * `backend/app/routers/admin.py`.
 */
export const SEED_ROWS: readonly RosterRow[] = Object.freeze([
  {
    id: 101,
    student_number: "2024-01234",
    full_name: "DELA CRUZ, Juan Miguel, S.",
    degree_program: "BS Computer Science",
    college: "CAS",
    year_level: 3,
    up_mail: "jmdelacruz@up.edu.ph",
    submitted_at: "2027-01-05T02:11:00Z",
    ref: "REG-2027-44102"
  },
  {
    id: 102,
    student_number: "2024-01234",
    full_name: "DELA CRUZ, Juan Migel, S.",
    degree_program: "BS Computer Science",
    college: "CAS",
    year_level: 3,
    up_mail: "jmdelacruz@up.edu.ph",
    submitted_at: "2027-01-05T06:47:00Z",
    ref: "REG-2027-51277"
  },
  {
    id: 103,
    student_number: "2023-08765",
    full_name: "REYES, Maria Isabel",
    degree_program: "BA Communication and Media Studies",
    college: "CAS",
    year_level: 2,
    up_mail: "mireyes@up.edu.ph",
    submitted_at: "2027-01-06T09:03:00Z",
    ref: "REG-2027-53018"
  },
  {
    id: 104,
    student_number: "2022-00341",
    full_name: "SANTOS, Paolo Ramirez",
    degree_program: "BS Accountancy",
    college: "SBM",
    year_level: 4,
    up_mail: "prsantos@up.edu.ph",
    submitted_at: "2027-01-06T11:22:00Z",
    ref: "REG-2027-53466"
  },
  {
    id: 105,
    student_number: "2025-00918",
    full_name: "LIM, Andrea Nicole, T.",
    degree_program: "BS Fisheries",
    college: "CFOS",
    year_level: 1,
    up_mail: "anlim@up.edu.ph",
    submitted_at: "2027-01-07T01:15:00Z",
    ref: "REG-2027-55109"
  },
  {
    id: 106,
    student_number: "2023-08765",
    full_name: "REYES, Maria Isabel",
    degree_program: "BA Communication and Media Studies",
    college: "CAS",
    year_level: 2,
    up_mail: "mireyes@up.edu.ph",
    submitted_at: "2027-01-07T03:40:00Z",
    ref: "REG-2027-55821"
  }
]);

export const nextRowId = (rows: readonly RosterRow[]): number =>
  rows.reduce((max, row) => Math.max(max, row.id), 0) + 1;

/** `REG-YYYY-NNNNN`, using the UTC year to match the backend. */
export const generateRef = (
  now: Date = new Date(),
  rand: () => number = Math.random
): string =>
  `REG-${now.getUTCFullYear()}-${String(Math.floor(rand() * 90000) + 10000)}`;
