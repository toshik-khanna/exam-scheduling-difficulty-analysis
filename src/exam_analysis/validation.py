"""
Data Validation Module
======================

Validates the integrity of difficulty rating records.

Component 1 (continued) of the research implementation.

Checks:
    - All rating values are integers in [1, 5]
    - No duplicate respondent IDs
    - All required columns present
    - Expected respondent counts (30 students, 5 teachers)
"""

from typing import Dict, List, Optional, Tuple


class ValidationError:
    """Represents a single validation error."""

    def __init__(self, respondent_id: str, field: str, message: str):
        self.respondent_id = respondent_id
        self.field = field
        self.message = message

    def __str__(self):
        return f"[{self.respondent_id}] {self.field}: {self.message}"

    def __repr__(self):
        return f"ValidationError({self.respondent_id!r}, {self.field!r}, {self.message!r})"


class ValidationReport:
    """Collects and summarizes validation results."""

    def __init__(self):
        self.errors: List[ValidationError] = []
        self.warnings: List[str] = []
        self.total_records: int = 0
        self.student_count: int = 0
        self.teacher_count: int = 0

    @property
    def is_valid(self) -> bool:
        """True if no errors were found."""
        return len(self.errors) == 0

    def add_error(self, respondent_id: str, field: str, message: str):
        self.errors.append(ValidationError(respondent_id, field, message))

    def add_warning(self, message: str):
        self.warnings.append(message)

    def summary(self) -> str:
        """Generate a human-readable summary."""
        lines = [
            f"Validation Report",
            f"{'=' * 50}",
            f"Total records:  {self.total_records}",
            f"Students:       {self.student_count}",
            f"Teachers:       {self.teacher_count}",
            f"Errors:         {len(self.errors)}",
            f"Warnings:       {len(self.warnings)}",
            f"Status:         {'PASSED' if self.is_valid else 'FAILED'}",
        ]

        if self.errors:
            lines.append(f"\nErrors:")
            for err in self.errors:
                lines.append(f"  - {err}")

        if self.warnings:
            lines.append(f"\nWarnings:")
            for warn in self.warnings:
                lines.append(f"  - {warn}")

        return "\n".join(lines)


def validate_records(
    records: List[Dict],
    expected_students: int = 30,
    expected_teachers: int = 5,
    min_rating: int = 1,
    max_rating: int = 5,
    strict_counts: bool = False,
) -> ValidationReport:
    """
    Validate all respondent records.

    Parameters
    ----------
    records : list of dict
        Records loaded by data_loader.load_ratings().
    expected_students : int
        Expected number of student respondents.
    expected_teachers : int
        Expected number of teacher respondents.
    min_rating : int
        Minimum valid difficulty rating.
    max_rating : int
        Maximum valid difficulty rating.

    Returns
    -------
    ValidationReport
        Contains all errors, warnings, and counts.
    """
    report = ValidationReport()
    report.total_records = len(records)

    subjects = ("M", "P", "C", "CS", "E")
    seen_ids = set()
    students = []
    teachers = []

    for record in records:
        rid = record.get("ID", "UNKNOWN")

        # Check for duplicate IDs
        if rid in seen_ids:
            report.add_error(rid, "ID", "Duplicate respondent ID")
        seen_ids.add(rid)

        # Check group assignment
        group = record.get("group")
        if group == "student":
            students.append(record)
        elif group == "teacher":
            teachers.append(record)
        else:
            report.add_error(rid, "group", f"Unknown group: {group}")

        # Validate each subject rating
        for subj in subjects:
            value = record.get(subj)
            if value is None:
                report.add_error(rid, subj, "Missing rating")
                continue

            if not isinstance(value, int):
                report.add_error(
                    rid, subj, f"Rating must be integer, got {type(value).__name__}"
                )
                continue

            if value < min_rating or value > max_rating:
                report.add_error(
                    rid, subj,
                    f"Rating {value} out of range [{min_rating}, {max_rating}]"
                )

    report.student_count = len(students)
    report.teacher_count = len(teachers)

    # Check expected counts
    if len(students) != expected_students:
        (report.add_error("DATASET", "students", f"Expected {expected_students} students, found {len(students)}") if strict_counts else report.add_warning(f"Expected {expected_students} students, found {len(students)}"))

    if len(teachers) != expected_teachers:
        (report.add_error("DATASET", "teachers", f"Expected {expected_teachers} teachers, found {len(teachers)}") if strict_counts else report.add_warning(f"Expected {expected_teachers} teachers, found {len(teachers)}"))

    total_expected = expected_students + expected_teachers
    if len(records) != total_expected:
        (report.add_error("DATASET", "total", f"Expected {total_expected} records, found {len(records)}") if strict_counts else report.add_warning(f"Expected {total_expected} total records, found {len(records)}"))

    return report
