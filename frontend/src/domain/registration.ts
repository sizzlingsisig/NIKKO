/**
 * Domain types for the registration flow and the admin roster.
 * Field names mirror the backend (`backend/app/schemas.py`, `routers/admin.py`)
 * so a future API pass swaps the mock store for real calls without reshaping.
 */

export const COLLEGES = ["SBM", "CAS", "CFOS", "SOT"] as const;
export type College = (typeof COLLEGES)[number];

export const YEAR_LEVELS = ["1", "2", "3", "4", "5", "6"] as const;

export const DEGREE_PROGRAM_SUGGESTIONS = [
  "BS Computer Science",
  "BS Biology",
  "BA Communication and Media Studies",
  "BS Accountancy",
  "BS Fisheries",
  "BS Chemistry"
] as const;

export type CollegeSlot = College | "";

/**
 * Narrows an untrusted string to the closed `College` union. Used at the store
 * boundary instead of a cast, so a hand-edited draft can never smuggle an
 * arbitrary college into the roster.
 */
export const toCollege = (value: string): College | null =>
  COLLEGES.find(college => college === value.trim()) ?? null;

/** The six fields the student confirms. Kept as strings for form binding. */
export interface RegistrationDraft {
  student_number: string;
  full_name: string;
  degree_program: string;
  college: CollegeSlot;
  year_level: string;
  up_mail: string;
}

/** A committed roster row, as the admin console sees it. */
export interface RosterRow {
  readonly id: number;
  readonly student_number: string;
  readonly full_name: string;
  readonly degree_program: string;
  readonly college: College;
  readonly year_level: number;
  readonly up_mail: string;
  /** UTC ISO-8601. Deduplication orders on this. */
  readonly submitted_at: string;
  readonly ref: string;
}

/** A roster row plus the dedupe verdict used for row highlighting. */
export interface AnnotatedRosterRow extends RosterRow {
  readonly is_latest: boolean;
}

export interface RosterStats {
  readonly raw: number;
  readonly unique: number;
  readonly collapsed: number;
}

export type ParseMode = "vector" | "raster";

/** Result of the (simulated) client-side parse pass. */
export interface ParsedForm5 {
  readonly fileName: string;
  readonly mode: ParseMode;
  /** Present only on the raster path. */
  readonly ocrConfidence?: number;
  readonly fields: RegistrationDraft;
}

/** Photo / signature preview. RAM only — never persisted (FR-2.4). */
export interface Attachment {
  readonly name: string;
  readonly size: number;
  /** Object URL or data URL of the local preview. */
  readonly url: string;
}

export type AttachmentKind = "photo" | "signature";

export const EMPTY_DRAFT: RegistrationDraft = Object.freeze({
  student_number: "",
  full_name: "",
  degree_program: "",
  college: "",
  year_level: "",
  up_mail: ""
});
