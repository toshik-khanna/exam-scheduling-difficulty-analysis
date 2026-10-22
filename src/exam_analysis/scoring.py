"""
Scoring Module
==============

Implements the consecutive-subject burden objective function from Khanna [1].

Component 4 of the research implementation.

Mathematical definition:

    S_r(π) = Σ_{i=1}^{4} D_{r,π_i} · D_{r,π_{i+1}}

where:
    r identifies the respondent,
    π identifies the examination order,
    D_{r,s} is respondent r's difficulty rating for subject s,
    π_i is the subject assigned to position i.

Reference values (original assumed scores M=5, P=5, C=4, CS=3, E=2):
    Baseline schedule (M, P, C, E, CS):   score = 59
    Optimal schedule  (M, CS, C, E, P):   score = 45
"""

from typing import Dict, List, Tuple

from . import SUBJECTS


def schedule_score(
    schedule: Tuple[str, ...],
    ratings: Dict[str, int],
) -> int:
    """
    Calculate the consecutive-subject burden score for one schedule and one
    respondent's ratings.

    Parameters
    ----------
    schedule : tuple of str
        Examination order, e.g. ("M", "P", "C", "E", "CS").
    ratings : dict
        Mapping from subject code to integer difficulty rating.

    Returns
    -------
    int
        The total scheduling score. Lower is better under the model.

    Examples
    --------
    >>> original = {"M": 5, "P": 5, "C": 4, "CS": 3, "E": 2}
    >>> schedule_score(("M", "P", "C", "E", "CS"), original)
    59
    >>> schedule_score(("M", "CS", "C", "E", "P"), original)
    45
    """
    total = 0
    for i in range(len(schedule) - 1):
        total += ratings[schedule[i]] * ratings[schedule[i + 1]]
    return total


def evaluate_all_schedules(
    schedules: List[Tuple[str, ...]],
    ratings: Dict[str, int],
) -> Dict[Tuple[str, ...], int]:
    """
    Evaluate every candidate schedule for one respondent.

    Parameters
    ----------
    schedules : list of tuple
        All 120 candidate examination orders.
    ratings : dict
        One respondent's difficulty ratings.

    Returns
    -------
    dict
        Mapping from schedule to score.
    """
    return {s: schedule_score(s, ratings) for s in schedules}


def find_minimum_score(
    schedules: List[Tuple[str, ...]],
    ratings: Dict[str, int],
) -> int:
    """
    Find the minimum achievable scheduling score for one respondent.

    Parameters
    ----------
    schedules : list of tuple
        All candidate examination orders.
    ratings : dict
        One respondent's difficulty ratings.

    Returns
    -------
    int
        The minimum scheduling score across all schedules.
    """
    return min(schedule_score(s, ratings) for s in schedules)


def find_optimal_schedules(
    schedules: List[Tuple[str, ...]],
    ratings: Dict[str, int],
) -> List[Tuple[str, ...]]:
    """
    Find all schedules that achieve the minimum score for one respondent.

    Parameters
    ----------
    schedules : list of tuple
        All candidate examination orders.
    ratings : dict
        One respondent's difficulty ratings.

    Returns
    -------
    list of tuple
        All schedules achieving the minimum score.
    """
    scores = evaluate_all_schedules(schedules, ratings)
    min_score = min(scores.values())
    return [s for s, v in scores.items() if v == min_score]


def verify_reversal_symmetry(
    schedule: Tuple[str, ...],
    ratings: Dict[str, int],
) -> bool:
    """
    Verify that a schedule and its reversal produce the same score.

    The scoring formula is symmetric because:
        S(π₁, π₂, ..., π₅) = Σ D_{π_i} · D_{π_{i+1}}
        S(π₅, π₄, ..., π₁) = Σ D_{π_{5-i}} · D_{π_{4-i}} = same sum

    Parameters
    ----------
    schedule : tuple of str
        An examination schedule.
    ratings : dict
        Difficulty ratings.

    Returns
    -------
    bool
        True if score equals reverse score.
    """
    forward = schedule_score(schedule, ratings)
    backward = schedule_score(tuple(reversed(schedule)), ratings)
    return forward == backward
