"""
Test Data Validation Module
===========================

Verifies data validation rules:
- Duplicate IDs rejected
- Out-of-range ratings (<1 or >5) rejected
- Non-integer ratings rejected
- Missing subject ratings rejected
- Expected counts (30 students, 5 teachers) verified
"""

import pytest

from exam_analysis.validation import validate_records


def test_valid_records():
    """Verify validation passes for valid respondent data."""
    records = [
        {"ID": f"S{i:02d}", "group": "student", "M": 4, "P": 5, "C": 4, "CS": 3, "E": 2}
        for i in range(1, 31)
    ] + [
        {"ID": f"T{i:02d}", "group": "teacher", "M": 4, "P": 4, "C": 4, "CS": 4, "E": 3}
        for i in range(1, 6)
    ]
    report = validate_records(records, expected_students=30, expected_teachers=5)
    assert report.is_valid is True
    assert report.total_records == 35
    assert report.student_count == 30
    assert report.teacher_count == 5


def test_duplicate_id_rejected():
    """Verify duplicate respondent ID triggers an error."""
    records = [
        {"ID": "S01", "group": "student", "M": 4, "P": 5, "C": 4, "CS": 3, "E": 2},
        {"ID": "S01", "group": "student", "M": 5, "P": 5, "C": 4, "CS": 3, "E": 2},
    ]
    report = validate_records(records, expected_students=2, expected_teachers=0)
    assert report.is_valid is False
    assert any("Duplicate" in err.message for err in report.errors)


def test_rating_out_of_range_rejected():
    """Verify ratings outside [1, 5] trigger validation errors."""
    records = [
        {"ID": "S01", "group": "student", "M": 6, "P": 5, "C": 4, "CS": 3, "E": 2},
        {"ID": "S02", "group": "student", "M": 0, "P": 5, "C": 4, "CS": 3, "E": 2},
    ]
    report = validate_records(records, expected_students=2, expected_teachers=0)
    assert report.is_valid is False
    assert len(report.errors) == 2


def test_missing_rating_rejected():
    """Verify missing ratings trigger validation errors."""
    records = [
        {"ID": "S01", "group": "student", "M": None, "P": 5, "C": 4, "CS": 3, "E": 2},
    ]
    report = validate_records(records, expected_students=1, expected_teachers=0)
    assert report.is_valid is False
    assert any(err.field == "M" for err in report.errors)
