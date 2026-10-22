"""
Test Individual Optimizer Module
================================

Verifies:
- Optimization of single respondent records
- Identification of baseline, selected, and minimum scores
- Optimality gap calculation: G_r = S_r(π_sel) - S_r* >= 0
- Tie detection
"""

import pytest

from exam_analysis import BASELINE_SCHEDULE, KHANNA_SELECTED_SCHEDULE
from exam_analysis.individual_optimizer import optimize_individual


def test_individual_optimization_structure():
    """Verify individual optimization returns expected fields and valid values."""
    record = {"ID": "S01", "group": "student", "M": 5, "P": 5, "C": 4, "CS": 3, "E": 2}
    result = optimize_individual(record)

    assert result.respondent_id == "S01"
    assert result.group == "student"
    assert result.baseline_score == 59
    assert result.selected_score == 45
    assert result.minimum_score == 45
    assert result.optimality_gap == 0
    assert result.optimal_count == 4
    assert result.reduction_pct == pytest.approx((59 - 45) / 59 * 100, rel=1e-3)


def test_optimality_gap_non_negative():
    """Verify optimality gap is always non-negative for arbitrary ratings."""
    record = {"ID": "T01", "group": "teacher", "M": 3, "P": 4, "C": 2, "CS": 5, "E": 1}
    result = optimize_individual(record)

    assert result.optimality_gap >= 0
    assert result.minimum_score <= result.selected_score
    assert result.minimum_score <= result.baseline_score
