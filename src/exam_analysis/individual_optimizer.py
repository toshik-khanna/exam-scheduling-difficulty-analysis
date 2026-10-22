"""
Individual Optimizer Module
============================

Identifies the optimal examination schedule(s) for each individual respondent.

Component 5 of the research implementation.

For each of the 35 respondents, evaluates all 120 timetables and records:
    - Baseline score (under the existing examination order)
    - Score of the schedule selected in Khanna [1]
    - Individual minimum score
    - Number of tied optimal schedules
    - Complete set of optimal arrangements
    - Individual optimality gap: G_r = S_r(π_selected) - S_r*
"""

from typing import Dict, List, Tuple

from .data_loader import get_ratings_vector
from .scoring import schedule_score, evaluate_all_schedules
from .timetable_generator import generate_all_schedules, schedule_to_string
from . import BASELINE_SCHEDULE, KHANNA_SELECTED_SCHEDULE


class IndividualResult:
    """Optimization results for a single respondent."""

    def __init__(
        self,
        respondent_id: str,
        group: str,
        ratings: Dict[str, int],
        baseline_score: int,
        selected_score: int,
        minimum_score: int,
        optimal_schedules: List[Tuple[str, ...]],
        all_scores: Dict[Tuple[str, ...], int],
    ):
        self.respondent_id = respondent_id
        self.group = group
        self.ratings = ratings
        self.baseline_score = baseline_score
        self.selected_score = selected_score
        self.minimum_score = minimum_score
        self.optimal_schedules = optimal_schedules
        self.optimal_count = len(optimal_schedules)
        self.all_scores = all_scores

        # Optimality gap: how much worse the selected schedule is compared
        # to the individual's true optimum
        self.optimality_gap = selected_score - minimum_score

        # Percentage reduction from baseline to minimum
        if baseline_score > 0:
            self.reduction_pct = (
                (baseline_score - minimum_score) / baseline_score * 100
            )
        else:
            self.reduction_pct = 0.0

    def __repr__(self):
        return (
            f"IndividualResult({self.respondent_id}: "
            f"baseline={self.baseline_score}, "
            f"selected={self.selected_score}, "
            f"min={self.minimum_score}, "
            f"gap={self.optimality_gap}, "
            f"optimal_count={self.optimal_count})"
        )


def optimize_individual(
    record: Dict,
    all_schedules: List[Tuple[str, ...]] = None,
    baseline: Tuple[str, ...] = None,
    selected: Tuple[str, ...] = None,
) -> IndividualResult:
    """
    Find all optimal schedules for one respondent.

    Parameters
    ----------
    record : dict
        Respondent record with ID, group, and subject ratings.
    all_schedules : list of tuple, optional
        All 120 candidate schedules. Generated if not provided.
    baseline : tuple of str, optional
        The baseline (existing) examination schedule.
    selected : tuple of str, optional
        The schedule selected in Khanna [1].

    Returns
    -------
    IndividualResult
        Complete optimization results for this respondent.
    """
    if all_schedules is None:
        all_schedules = generate_all_schedules()
    if baseline is None:
        baseline = BASELINE_SCHEDULE
    if selected is None:
        selected = KHANNA_SELECTED_SCHEDULE

    ratings = get_ratings_vector(record)
    scores = evaluate_all_schedules(all_schedules, ratings)

    baseline_score = scores[baseline]
    selected_score = scores[selected]
    min_score = min(scores.values())
    optimal = [s for s, v in scores.items() if v == min_score]

    return IndividualResult(
        respondent_id=record["ID"],
        group=record["group"],
        ratings=ratings,
        baseline_score=baseline_score,
        selected_score=selected_score,
        minimum_score=min_score,
        optimal_schedules=optimal,
        all_scores=scores,
    )


def optimize_all_individuals(
    records: List[Dict],
) -> List[IndividualResult]:
    """
    Run individual optimization for all respondents.

    Parameters
    ----------
    records : list of dict
        All 35 respondent records.

    Returns
    -------
    list of IndividualResult
        Optimization results for each respondent.
    """
    all_schedules = generate_all_schedules()
    results = []

    for record in records:
        result = optimize_individual(record, all_schedules)
        results.append(result)

    return results


def format_individual_summary(results: List[IndividualResult]) -> str:
    """
    Format individual optimization results as a readable summary.

    Parameters
    ----------
    results : list of IndividualResult
        Results from optimize_all_individuals().

    Returns
    -------
    str
        Formatted summary table.
    """
    header = "\nIndividual Optimization Summary"
    sep = "=" * 90
    col_header = (
        f"{'ID':<6} {'Group':<9} {'Baseline':>9} {'Selected':>9} "
        f"{'Minimum':>8} {'Gap':>5} {'Reduction%':>11} {'#Optimal':>9}"
    )
    lines = [header, sep, col_header, "-" * 90]

    for r in results:
        lines.append(
            f"{r.respondent_id:<6} {r.group:<9} {r.baseline_score:>9d} "
            f"{r.selected_score:>9d} {r.minimum_score:>8d} "
            f"{r.optimality_gap:>5d} {r.reduction_pct:>10.2f}% "
            f"{r.optimal_count:>9d}"
        )

    lines.append(sep)

    # Summary statistics
    gaps = [r.optimality_gap for r in results]
    lines.append(f"\nMean optimality gap:   {sum(gaps) / len(gaps):.2f}")
    lines.append(f"Max optimality gap:    {max(gaps)}")
    lines.append(f"Respondents at optimum (gap=0): "
                 f"{sum(1 for g in gaps if g == 0)}/{len(gaps)}")

    return "\n".join(lines)
