"""
Test Timetable Permutations
===========================

Verifies mathematical properties of timetable enumeration:
- Exactly 5! = 120 valid permutations
- Each permutation contains five unique subjects (no omission, no repetition)
- Reversal produces a valid distinct schedule (except if palindromic, which none are)
"""

import pytest
from itertools import permutations

from exam_analysis import SUBJECTS
from exam_analysis.timetable_generator import (
    generate_all_schedules,
    get_reversed_schedule,
    validate_schedule,
)


def test_number_of_permutations():
    """Verify that exactly 120 unique schedules are generated."""
    schedules = generate_all_schedules()
    assert len(schedules) == 120
    assert len(set(schedules)) == 120


def test_each_permutation_has_five_unique_subjects():
    """Verify that every permutation contains all 5 subjects with no repetition."""
    schedules = generate_all_schedules()
    expected_set = set(SUBJECTS)
    for sched in schedules:
        assert len(sched) == 5
        assert set(sched) == expected_set
        assert validate_schedule(sched) is True


def test_schedule_reversal():
    """Verify schedule reversal properties."""
    sched = ("M", "CS", "C", "E", "P")
    rev = get_reversed_schedule(sched)
    assert rev == ("P", "E", "C", "CS", "M")
    assert get_reversed_schedule(rev) == sched
    assert validate_schedule(rev) is True
