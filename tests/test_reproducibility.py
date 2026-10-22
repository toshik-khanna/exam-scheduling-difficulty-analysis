"""
Test Reproducibility Module
===========================

Automated verification tests that ensure the computational implementation
reproduces the exact numerical results reported in the manuscript:

Table 8 / Means:
    - Students: M=4.43, P=4.67, C=3.90, CS=3.80, E=2.90
    - Teachers: M=4.40, P=4.60, C=3.80, CS=3.80, E=2.80
    - Combined: M=4.43, P=4.66, C=3.89, CS=3.80, E=2.89

Group Scheduling Scores:
    - Students: Baseline=1,833, Minimum=1,689, Selected=1,689, Reduction=7.85%
    - Teachers: Baseline=294, Minimum=273, Selected=274, Reduction=7.14%
    - Combined: Baseline=2,127, Minimum=1,963, Selected=1,963, Reduction=7.71%

Optimal Timetables:
    - Combined optimal count == 2 (M->CS->C->E->P and P->E->C->CS->M)
    - Teachers optimal differs from combined
"""

import os
import pytest

from exam_analysis import BASELINE_SCHEDULE, KHANNA_SELECTED_SCHEDULE, SUBJECTS
from exam_analysis.data_loader import load_ratings, split_by_group
from exam_analysis.group_optimizer import optimize_all_groups
from exam_analysis.statistics import comparative_statistics
from exam_analysis.timetable_generator import generate_all_schedules, get_reversed_schedule


@pytest.fixture(scope="module")
def dataset():
    filepath = os.path.join(
        os.path.dirname(__file__), "..", "data", "survey", "difficulty_ratings.csv"
    )
    records = load_ratings(filepath)
    students, teachers = split_by_group(records)
    all_schedules = generate_all_schedules()
    groups = optimize_all_groups(records, all_schedules)
    stats = comparative_statistics(students, teachers)
    return {
        "records": records,
        "students": students,
        "teachers": teachers,
        "all_schedules": all_schedules,
        "groups": groups,
        "stats": stats,
    }


def test_respondent_counts(dataset):
    """Verify respondent sample sizes."""
    assert len(dataset["records"]) == 35
    assert len(dataset["students"]) == 30
    assert len(dataset["teachers"]) == 5


def test_descriptive_means(dataset):
    """Verify descriptive means match manuscript Table 8."""
    expected_means = {
        "students": {"M": 4.43, "P": 4.67, "C": 3.90, "CS": 3.80, "E": 2.90},
        "teachers": {"M": 4.40, "P": 4.60, "C": 3.80, "CS": 3.80, "E": 2.80},
        "combined": {"M": 4.43, "P": 4.66, "C": 3.89, "CS": 3.80, "E": 2.89},
    }
    for group_key, exp_group in expected_means.items():
        for subj, exp_val in exp_group.items():
            actual = dataset["stats"][group_key][subj]["mean"]
            assert actual == pytest.approx(exp_val, abs=0.01), (
                f"Mismatch for {group_key} {subj}: got {actual}, expected {exp_val}"
            )


def test_group_scheduling_scores(dataset):
    """Verify exact group baseline, selected, and minimum scores."""
    groups = dataset["groups"]

    # Students
    assert groups["students"].baseline_score == 1833
    assert groups["students"].selected_score == 1689
    assert groups["students"].minimum_score == 1689
    assert groups["students"].reduction_pct == pytest.approx(7.85, abs=0.02)

    # Teachers
    assert groups["teachers"].baseline_score == 294
    assert groups["teachers"].selected_score == 274
    assert groups["teachers"].minimum_score == 273
    assert groups["teachers"].reduction_pct == pytest.approx(7.14, abs=0.02)

    # Combined
    assert groups["combined"].baseline_score == 2127
    assert groups["combined"].selected_score == 1963
    assert groups["combined"].minimum_score == 1963
    assert groups["combined"].reduction_pct == pytest.approx(7.71, abs=0.02)


def test_combined_optimal_timetables(dataset):
    """Verify combined optimal timetables and count."""
    comb = dataset["groups"]["combined"]
    assert comb.optimal_count == 2
    assert KHANNA_SELECTED_SCHEDULE in comb.optimal_schedules
    assert get_reversed_schedule(KHANNA_SELECTED_SCHEDULE) in comb.optimal_schedules


def test_teachers_optimal_differs_from_students(dataset):
    """Verify teachers' joint optimum differs from students' optimum."""
    t_opt = dataset["groups"]["teachers"].optimal_schedules
    assert KHANNA_SELECTED_SCHEDULE not in t_opt
    assert dataset["groups"]["teachers"].selected_score == 274
    assert dataset["groups"]["teachers"].minimum_score == 273


def test_rating_perturbation_sensitivity(dataset):
    """Verify exact perturbation stability properties requested for publication."""
    from exam_analysis.sensitivity import evaluate_rating_sensitivity
    sens = evaluate_rating_sensitivity(dataset["records"], dataset["all_schedules"])

    assert sens["total_perturbations"] == 301
    assert sens["optimal_retained_count"] == 301
    assert sens["unchanged_optima_set_count"] == 295
    assert sens["additional_ties_count"] == 6
    assert sens["stability_rate_pct"] == 100.0
    assert sens["summary_statement"] == (
        "Across 301 valid single-point perturbations of individual difficulty ratings, "
        "the two original aggregate-optimal schedules remained optimal in every case. "
        "In six perturbations, additional schedules also attained the minimum score."
    )
