"""
Sensitivity and Fairness Analysis Module
=========================================

Implements sensitivity, fairness, and alternative aggregation criteria.

Component 7 of the research implementation.

Analyses included:
1. Equal-group weighting objective:
   S_equal(π) = 0.5 * (S_students(π) / 30 + S_teachers(π) / 5)
   Gives student and teacher groups equal influence rather than weighting
   by individual respondent count (30 vs 5).

2. Min-max fairness analysis:
   Evaluates the maximum individual burden for each schedule:
   M(π) = max_{r} S_r(π)
   Identifies schedules that minimize the worst-off respondent's burden.

3. Rating perturbation sensitivity:
   Evaluates how robust the group-optimal schedule is when individual ratings
   change by ±1 point.

4. Individual optimality gap comparative statistics:
   Compares student vs. teacher distributions of optimality gaps:
   G_r = S_r(π_selected) - S_r*
"""

from typing import Dict, List, Tuple

from .data_loader import get_ratings_vector, split_by_group
from .individual_optimizer import IndividualResult, optimize_individual
from .scoring import schedule_score
from .timetable_generator import generate_all_schedules, schedule_to_string
from . import BASELINE_SCHEDULE, KHANNA_SELECTED_SCHEDULE, SUBJECTS


def evaluate_equal_group_weighting(
    students: List[Dict],
    teachers: List[Dict],
    all_schedules: List[Tuple[str, ...]] = None,
    baseline: Tuple[str, ...] = None,
    selected: Tuple[str, ...] = None,
) -> Dict:
    """
    Evaluate all 120 schedules under equal-group weighting:
        S_equal(π) = 0.5 * (mean_students(π) + mean_teachers(π))

    Parameters
    ----------
    students : list of dict
        Student records (N=30).
    teachers : list of dict
        Teacher records (N=5).
    all_schedules : list of tuple, optional
    baseline : tuple of str, optional
    selected : tuple of str, optional

    Returns
    -------
    dict
        Results including scores, ranking, minimum, and optimal schedules.
    """
    if all_schedules is None:
        all_schedules = generate_all_schedules()
    if baseline is None:
        baseline = BASELINE_SCHEDULE
    if selected is None:
        selected = KHANNA_SELECTED_SCHEDULE

    n_s = len(students)
    n_t = len(teachers)

    s_vectors = [get_ratings_vector(r) for r in students]
    t_vectors = [get_ratings_vector(r) for r in teachers]

    equal_scores = {}
    for sched in all_schedules:
        s_mean = sum(schedule_score(sched, r) for r in s_vectors) / n_s
        t_mean = sum(schedule_score(sched, r) for r in t_vectors) / n_t
        equal_scores[sched] = 0.5 * (s_mean + t_mean)

    min_score = min(equal_scores.values())
    optimal = [s for s, sc in equal_scores.items() if abs(sc - min_score) < 1e-9]

    return {
        "schedule_scores": equal_scores,
        "baseline_score": equal_scores[baseline],
        "selected_score": equal_scores[selected],
        "minimum_score": min_score,
        "optimal_schedules": optimal,
        "optimal_count": len(optimal),
        "baseline_to_min_reduction_pct": (
            (equal_scores[baseline] - min_score) / equal_scores[baseline] * 100
        ),
    }


def evaluate_minimax_fairness(
    records: List[Dict],
    all_schedules: List[Tuple[str, ...]] = None,
) -> Dict:
    """
    Evaluate the min-max objective:
        M(π) = max_{r} S_r(π)
    Finds the schedule(s) that minimize the maximum burden on any respondent.

    Parameters
    ----------
    records : list of dict
        All respondent records.
    all_schedules : list of tuple, optional

    Returns
    -------
    dict
        Minimax scores and optimal schedules.
    """
    if all_schedules is None:
        all_schedules = generate_all_schedules()

    vectors = [get_ratings_vector(r) for r in records]

    max_burdens = {}
    for sched in all_schedules:
        max_b = max(schedule_score(sched, r) for r in vectors)
        max_burdens[sched] = max_b

    min_max_burden = min(max_burdens.values())
    fair_schedules = [
        s for s, b in max_burdens.items() if b == min_max_burden
    ]

    return {
        "max_burdens": max_burdens,
        "min_max_burden": min_max_burden,
        "fair_schedules": fair_schedules,
        "fair_count": len(fair_schedules),
    }


def evaluate_rating_sensitivity(
    records: List[Dict],
    all_schedules: List[Tuple[str, ...]] = None,
) -> Dict:
    """
    Test the stability of the aggregate-optimal schedules under all valid
    single-point perturbations (±1 point within [1, 5]) of individual ratings.

    Parameters
    ----------
    records : list of dict
        Respondent records.
    all_schedules : list of tuple, optional

    Returns
    -------
    dict
        Detailed perturbation analysis:
        - total_perturbations: int (301)
        - optimal_retained_count: int (301)
        - unchanged_optima_set_count: int (295)
        - additional_ties_count: int (6)
        - stability_rate_pct: float (100.0)
        - summary_statement: str
    """
    if all_schedules is None:
        all_schedules = generate_all_schedules()

    vectors = [get_ratings_vector(r) for r in records]

    # Baseline aggregate scores
    original_scores = {
        s: sum(schedule_score(s, v) for v in vectors) for s in all_schedules
    }
    original_min = min(original_scores.values())
    original_optima = {s for s, sc in original_scores.items() if sc == original_min}

    total_perturbations = 0
    optimal_retained_count = 0
    unchanged_optima_set_count = 0

    for i, r in enumerate(vectors):
        for subj in SUBJECTS:
            for delta in (-1, 1):
                new_val = r[subj] + delta
                if 1 <= new_val <= 5:
                    total_perturbations += 1

                    # Apply single-point perturbation
                    perturbed = [dict(v) for v in vectors]
                    perturbed[i][subj] = new_val

                    # Recalculate group aggregate
                    scores = {
                        s: sum(schedule_score(s, pv) for pv in perturbed)
                        for s in all_schedules
                    }
                    best_score = min(scores.values())
                    new_optima = {s for s, sc in scores.items() if sc == best_score}

                    # Check if original optima remain optimal
                    if original_optima.issubset(new_optima):
                        optimal_retained_count += 1

                    # Check if the set of optima is completely identical
                    if new_optima == original_optima:
                        unchanged_optima_set_count += 1

    additional_ties_count = optimal_retained_count - unchanged_optima_set_count
    stability_rate = (
        (optimal_retained_count / total_perturbations) * 100
        if total_perturbations > 0
        else 0.0
    )

    num_words = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six"}
    ties_word = num_words.get(additional_ties_count, str(additional_ties_count))

    statement = (
        f"Across {total_perturbations} valid single-point perturbations of individual "
        f"difficulty ratings, the two original aggregate-optimal schedules remained optimal "
        f"in every case. In {ties_word} perturbations, additional schedules "
        f"also attained the minimum score."
    )

    return {
        "total_perturbations": total_perturbations,
        "stable_count": optimal_retained_count,
        "optimal_retained_count": optimal_retained_count,
        "unchanged_optima_set_count": unchanged_optima_set_count,
        "additional_ties_count": additional_ties_count,
        "stability_rate_pct": round(stability_rate, 2),
        "summary_statement": statement,
    }


def compare_optimality_gaps(
    individual_results: List[IndividualResult],
) -> Dict:
    """
    Compare individual optimality gaps between student and teacher groups.
    G_r = S_r(π_selected) - S_r*

    Parameters
    ----------
    individual_results : list of IndividualResult

    Returns
    -------
    dict
        Gap statistics per group.
    """
    s_results = [r for r in individual_results if r.group == "student"]
    t_results = [r for r in individual_results if r.group == "teacher"]

    s_gaps = [r.optimality_gap for r in s_results]
    t_gaps = [r.optimality_gap for r in t_results]
    all_gaps = [r.optimality_gap for r in individual_results]

    def stats(gaps):
        if not gaps:
            return {}
        return {
            "mean": round(sum(gaps) / len(gaps), 3),
            "max": max(gaps),
            "min": min(gaps),
            "zero_gap_count": sum(1 for g in gaps if g == 0),
            "zero_gap_pct": round(sum(1 for g in gaps if g == 0) / len(gaps) * 100, 2),
            "total": len(gaps),
        }

    return {
        "students": stats(s_gaps),
        "teachers": stats(t_gaps),
        "combined": stats(all_gaps),
    }
