"""
Group Optimizer Module
======================

Implements group-level examination timetable optimization.

Component 6 of the research implementation.

The aggregate scheduling score of timetable π for group G is:
    S_G(π) = Σ_{r ∈ G} S_r(π)

Evaluates all 120 candidate timetables for:
    - Students (30 respondents)
    - Teachers (5 respondents)
    - Combined sample (35 respondents)

Preserves all tied optimal schedules (including reversal symmetries).
"""

from typing import Dict, List, NamedTuple, Tuple

from .data_loader import get_ratings_vector, split_by_group
from .scoring import schedule_score
from .timetable_generator import generate_all_schedules, schedule_to_string
from . import BASELINE_SCHEDULE, KHANNA_SELECTED_SCHEDULE


class GroupOptimizationResult:
    """Stores group-level optimization results."""

    def __init__(
        self,
        group_name: str,
        respondent_count: int,
        all_schedules: List[Tuple[str, ...]],
        schedule_scores: Dict[Tuple[str, ...], int],
        baseline_schedule: Tuple[str, ...],
        selected_schedule: Tuple[str, ...],
    ):
        self.group_name = group_name
        self.respondent_count = respondent_count
        self.all_schedules = all_schedules
        self.schedule_scores = schedule_scores
        self.baseline_schedule = baseline_schedule
        self.selected_schedule = selected_schedule

        self.baseline_score = schedule_scores[baseline_schedule]
        self.selected_score = schedule_scores[selected_schedule]
        self.minimum_score = min(schedule_scores.values())

        # All schedules achieving the minimum score
        self.optimal_schedules = [
            s for s, score in schedule_scores.items() if score == self.minimum_score
        ]
        self.optimal_count = len(self.optimal_schedules)

        # Baseline-to-minimum reduction percentage
        if self.baseline_score > 0:
            self.reduction_pct = (
                (self.baseline_score - self.minimum_score) / self.baseline_score * 100
            )
        else:
            self.reduction_pct = 0.0

        # Mean score per respondent
        self.mean_baseline = self.baseline_score / respondent_count
        self.mean_minimum = self.minimum_score / respondent_count
        self.mean_selected = self.selected_score / respondent_count

    def rank_schedules(self, ascending: bool = True) -> List[Tuple[Tuple[str, ...], int]]:
        """Return schedules sorted by aggregate score."""
        return sorted(
            self.schedule_scores.items(),
            key=lambda item: item[1],
            reverse=not ascending,
        )

    def summary(self) -> str:
        """Formatted summary text."""
        lines = [
            f"Group: {self.group_name}",
            f"Respondents: {self.respondent_count}",
            f"Baseline score: {self.baseline_score} (mean {self.mean_baseline:.2f})",
            f"Selected score: {self.selected_score} (mean {self.mean_selected:.2f})",
            f"Minimum score:  {self.minimum_score} (mean {self.mean_minimum:.2f})",
            f"Reduction:      {self.reduction_pct:.2f}%",
            f"Optimal count:  {self.optimal_count}",
            "Optimal schedules:",
        ]
        for s in self.optimal_schedules:
            lines.append(f"  - {schedule_to_string(s)}")
        return "\n".join(lines)


def optimize_group(
    records: List[Dict],
    group_name: str,
    all_schedules: List[Tuple[str, ...]] = None,
    baseline: Tuple[str, ...] = None,
    selected: Tuple[str, ...] = None,
) -> GroupOptimizationResult:
    """
    Evaluate aggregate scores for all 120 schedules for a specific group of records.

    Parameters
    ----------
    records : list of dict
        Respondent records.
    group_name : str
        Display name for the group (e.g. 'Students', 'Teachers', 'Combined').
    all_schedules : list of tuple, optional
        Candidate schedules.
    baseline : tuple of str, optional
        Baseline schedule.
    selected : tuple of str, optional
        Previously selected schedule.

    Returns
    -------
    GroupOptimizationResult
    """
    if all_schedules is None:
        all_schedules = generate_all_schedules()
    if baseline is None:
        baseline = BASELINE_SCHEDULE
    if selected is None:
        selected = KHANNA_SELECTED_SCHEDULE

    if not records:
        raise ValueError(f"Cannot optimize empty group '{group_name}'")

    rating_vectors = [get_ratings_vector(r) for r in records]

    # Precompute aggregate score for every schedule
    schedule_scores = {}
    for sched in all_schedules:
        total = sum(schedule_score(sched, r) for r in rating_vectors)
        schedule_scores[sched] = total

    return GroupOptimizationResult(
        group_name=group_name,
        respondent_count=len(records),
        all_schedules=all_schedules,
        schedule_scores=schedule_scores,
        baseline_schedule=baseline,
        selected_schedule=selected,
    )


def optimize_all_groups(
    records: List[Dict],
    all_schedules: List[Tuple[str, ...]] = None,
) -> Dict[str, GroupOptimizationResult]:
    """
    Run group optimization for Students, Teachers, and Combined populations.

    Parameters
    ----------
    records : list of dict
        All respondent records.
    all_schedules : list of tuple, optional
        Candidate schedules.

    Returns
    -------
    dict
        Mapping from group key ('students', 'teachers', 'combined') to GroupOptimizationResult.
    """
    if all_schedules is None:
        all_schedules = generate_all_schedules()

    students, teachers = split_by_group(records)

    return {
        "students": optimize_group(students, "Students (30)", all_schedules),
        "teachers": optimize_group(teachers, "Teachers (5)", all_schedules),
        "combined": optimize_group(records, "Combined (35)", all_schedules),
    }
