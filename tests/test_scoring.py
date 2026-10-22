"""
Test Scoring Module
===================

Verifies the mathematical consecutive-burden scoring function:
    S_r(π) = Σ_{i=1}^{4} D_{r,π_i} · D_{r,π_{i+1}}

Regression tests from Khanna [1]:
- Assumed scores {M:5, P:5, C:4, CS:3, E:2}
- Baseline schedule (M, P, C, E, CS) == 59
- Khanna [1] selected schedule (M, CS, C, E, P) == 45
- Schedule reversal symmetry: S(π) == S(reversed(π)) for all 120 schedules
"""

from itertools import permutations
import pytest

from exam_analysis import (
    BASELINE_SCHEDULE,
    KHANNA_SELECTED_SCHEDULE,
    ORIGINAL_ASSUMED_SCORES,
    SUBJECTS,
)
from exam_analysis.scoring import (
    evaluate_all_schedules,
    find_minimum_score,
    find_optimal_schedules,
    schedule_score,
    verify_reversal_symmetry,
)
from exam_analysis.timetable_generator import generate_all_schedules


def test_original_baseline_score():
    """Verify original baseline score equals 59 under Khanna [1] assumed ratings."""
    # M*P + P*C + C*E + E*CS = 5*5 + 5*4 + 4*2 + 2*3 = 25 + 20 + 8 + 6 = 59
    score = schedule_score(BASELINE_SCHEDULE, ORIGINAL_ASSUMED_SCORES)
    assert score == 59


def test_original_selected_minimum_score():
    """Verify Khanna [1] selected schedule score equals 45."""
    # M*CS + CS*C + C*E + E*P = 5*3 + 3*4 + 4*2 + 2*5 = 15 + 12 + 8 + 10 = 45
    score = schedule_score(KHANNA_SELECTED_SCHEDULE, ORIGINAL_ASSUMED_SCORES)
    assert score == 45


def test_original_assumed_minimum():
    """Verify minimum achievable score is 45 and exactly 4 schedules achieve it."""
    schedules = generate_all_schedules()
    min_score = find_minimum_score(schedules, ORIGINAL_ASSUMED_SCORES)
    assert min_score == 45

    optimal_schedules = find_optimal_schedules(schedules, ORIGINAL_ASSUMED_SCORES)
    assert len(optimal_schedules) == 4
    assert KHANNA_SELECTED_SCHEDULE in optimal_schedules


def test_reversal_symmetry_all_schedules():
    """Verify that every one of the 120 schedules has identical score to its reverse."""
    schedules = generate_all_schedules()
    for sched in schedules:
        assert verify_reversal_symmetry(sched, ORIGINAL_ASSUMED_SCORES) is True
