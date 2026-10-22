"""Additional regression tests for the 35-record research analysis."""
from pathlib import Path
import pytest
from exam_analysis.data_loader import load_ratings, split_by_group
from exam_analysis.validation import validate_records
from exam_analysis.sensitivity import evaluate_equal_group_weighting, evaluate_minimax_fairness
from exam_analysis.timetable_generator import generate_all_schedules

DATA=Path(__file__).resolve().parents[1] / "data" / "survey" / "difficulty_ratings.csv"

def test_strict_counts_reject_incomplete_dataset():
    records=load_ratings(str(DATA))
    report=validate_records(records[:-1], strict_counts=True)
    assert not report.is_valid

def test_equal_group_weighting_regression():
    records=load_ratings(str(DATA))
    students,teachers=split_by_group(records)
    result=evaluate_equal_group_weighting(students,teachers,generate_all_schedules())
    assert result["minimum_score"]==pytest.approx(55.5166666667)
    assert result["selected_score"]==pytest.approx(55.55)
    assert result["optimal_count"]==2

def test_minimax_regression():
    records=load_ratings(str(DATA))
    result=evaluate_minimax_fairness(records,generate_all_schedules())
    assert result["min_max_burden"]==70
    assert result["fair_count"]==12
