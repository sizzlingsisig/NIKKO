/**
 * Field rules and the verbatim student-facing error copy.
 *
 * Wording is duplicated from the prototype `RULES` object and from
 * `backend/app/schemas.py` so the messages a student reads here are
 * byte-identical to the ones the API returns.
 */

import type { RegistrationDraft } from "./registration";

// Upload ceilings. These MUST track `MAX_ARTIFACT_BYTES` in
// `backend/app/config.py` — the API enforces the same numbers server-side and
// answers 413 for anything larger, so a frontend-only bump would accept a file
// the backend then refuses. Kept as named constants so the pairing is greppable.
export const MAX_PDF_BYTES = 10 * 1024 * 1024;
export const MAX_IMAGE_BYTES = 5 * 1024 * 1024;

/** Tesseract mean-confidence floor below which the manual-review modal fires. */
export const OCR_CONFIDENCE_THRESHOLD = 75;

interface FieldRule {
  re: RegExp;
  message: string;
}

export const RULES = {
  student_number: {
    re: /^20\d{2}-\d{5}$/,
    message: "Must match format 20YY-XXXXX (e.g., 2024-01234)."
  },
  full_name: { re: /\S/, message: "Please enter your full legal name." },
  degree_program: { re: /\S/, message: "Please enter your degree program." },
  college: { re: /^(SBM|CAS|CFOS|SOT)$/, message: "Select your college unit." },
  year_level: { re: /^[1-6]$/, message: "Year level must be between 1 and 6." },
  up_mail: {
    re: /^[a-zA-Z0-9._%+-]+@up\.edu\.ph$/,
    message: "Must be a valid @up.edu.ph address."
  }
} as const satisfies Record<string, FieldRule>;

export type FieldKey = keyof typeof RULES;

/**
 * Declaration order, spelled out rather than derived from `Object.keys` so the
 * order is part of the contract (the parse log and error focus walk it) and the
 * compiler checks it against `FieldKey`.
 */
export const FIELD_KEYS = [
  "student_number",
  "full_name",
  "degree_program",
  "college",
  "year_level",
  "up_mail"
] as const satisfies readonly FieldKey[];

export const FIELD_LABELS: Record<FieldKey, string> = {
  student_number: "Student Number",
  full_name: "Full Name (Surname, First Name, Middle Name)",
  degree_program: "Degree Program",
  college: "College Unit",
  year_level: "Year Level",
  up_mail: "UP Mail Address"
};

/** Per-field provenance note shown under each input (FR-1.3 / FR-2). */
export const SOURCE_NOTES = {
  vector: "source: text-layer extraction",
  raster: "source: OCR (low confidence, please verify)"
} as const;

export const isFieldValid = (key: FieldKey, value: string): boolean =>
  RULES[key].re.test(value.trim());

export const fieldError = (key: FieldKey, value: string): string =>
  isFieldValid(key, value) ? "" : RULES[key].message;

/** Returns the keys that are currently invalid, in declaration order. */
export const invalidFieldKeys = (
  draft: Readonly<RegistrationDraft>
): readonly FieldKey[] =>
  FIELD_KEYS.filter(key => !isFieldValid(key, draft[key]));

export const isDraftValid = (draft: Readonly<RegistrationDraft>): boolean =>
  invalidFieldKeys(draft).length === 0;

export const isPdf = (name: string, type: string): boolean =>
  /\.pdf$/i.test(name) || type === "application/pdf";

export const isImage = (type: string): boolean => type.startsWith("image/");
