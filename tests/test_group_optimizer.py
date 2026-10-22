"""
Test Group Optimizer Module
===========================

Verifies group optimization calculations and mathematical properties:
- Preservation of tied solutions (both forward and reversed schedules)
- Aggregation correctness: S_G(π) = Σ S_r(π)
- Ranking of schedules
"""

import pytest

from exam_analysis import BASELINE_SCHEDULE, KHANNA_SELECTED_SCHEDULE
from exam_analysis.group_optimizer import optimize_group


def test_group_aggregation_correctness():
    """Verify group score equals sum of individual respondent scores."""
    records = [
        {"ID": "S01", "group": "student", "M": 5, "P": 5, "C": 4, "CS": 3, "E": 2},
        {"ID": "S02", "group": "student", "M": 4, "P": 4, "C": 3, "CS": 3, "E": 2},
    ]
    res = optimize_group(records, "Test Group")

    # S01: baseline 59, selected 45
    # S02: baseline 4*4 + 4*3 + 3*2 + 2*3 = 16 + 12 + 6 + 6 = 40
    #      selected 4*3 + 3*3 + 3*2 + 2*4 = 12 + 9 + 6 + 8 = 35
    assert res.baseline_score == 59 + 40
    assert res.selected_score == 45 + 35
    assert res.respondent_count == 2


def test_reversal_symmetry_preserved_in_optima():
    """Verify every optimal schedule has its reverse also in the optima."""
    records = [
        {"ID": "S01", "group": "student", "M": 5, "P": 5, "C": 4, "CS": 3, "E": 2},
        {"ID": "S02", "group": "student", "M": 4, "P": 5, "C": 4, "CS": 4, "E": 3},
    ]
    res = optimize_group(records, "Test Group")

    for opt_sched in res.optimal_schedules:
        rev_sched = tuple(reversed(opt_sched))
        assert rev_sched in res.optimal_schedules
