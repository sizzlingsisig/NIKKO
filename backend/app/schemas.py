"""Request models with the exact FR-2 validation messages.

The prototype (`form5_portal_prototype.html` RULES) owns the wording the
student sees, so the messages here are copied verbatim rather than
reworded.
"""

import re

from pydantic import BaseModel, field_validator

STUDENT_NUMBER_PATTERN = r"20\d{2}-\d{5}"
UP_MAIL_PATTERN = r"[a-zA-Z0-9._%+-]+@up\.edu\.ph"
SHA256_PATTERN = r"[0-9a-fA-F]{64}"

COLLEGES = ("SBM", "CAS", "CFOS", "SOT")


class RegistrationIn(BaseModel):
    """A Step-2 submission: the six roster fields plus RA 10173 consent."""

    student_number: str
    full_name: str
    degree_program: str
    college: str
    year_level: int
    up_mail: str
    consent: bool = False

    @field_validator("student_number")
    @classmethod
    def _check_student_number(cls, value: str) -> str:
        if not re.fullmatch(STUDENT_NUMBER_PATTERN, value):
            raise ValueError("Must match format 20YY-XXXXX (e.g., 2024-01234).")
        return value

    @field_validator("full_name")
    @classmethod
    def _check_full_name(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Please enter your full legal name.")
        return cleaned

    @field_validator("degree_program")
    @classmethod
    def _check_degree_program(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Please enter your degree program.")
        return cleaned

    @field_validator("college")
    @classmethod
    def _check_college(cls, value: str) -> str:
        if value not in COLLEGES:
            raise ValueError("Select your college unit.")
        return value

    @field_validator("year_level")
    @classmethod
    def _check_year_level(cls, value: int) -> int:
        if not 1 <= value <= 6:
            raise ValueError("Year level must be between 1 and 6.")
        return value

    @field_validator("up_mail")
    @classmethod
    def _check_up_mail(cls, value: str) -> str:
        if not re.fullmatch(UP_MAIL_PATTERN, value):
            raise ValueError("Must be a valid @up.edu.ph address.")
        return value

    @field_validator("consent")
    @classmethod
    def _check_consent(cls, value: bool) -> bool:
        if not value:
            raise ValueError("RA 10173 consent is required.")
        return value


class ArtifactClaim(BaseModel):
    """Client's account of one uploaded artifact (FR-5: S3 first, then DB)."""

    kind: str
    sha256: str
    mime: str

    @field_validator("sha256")
    @classmethod
    def _check_sha256(cls, value: str) -> str:
        if not re.fullmatch(SHA256_PATTERN, value):
            raise ValueError("Must be a 64-character hexadecimal sha256 digest.")
        return value.lower()
