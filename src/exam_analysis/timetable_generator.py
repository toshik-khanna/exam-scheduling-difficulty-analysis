"""
Timetable Generator Module
===========================

Generates all valid examination schedules using exhaustive permutation
enumeration.

Component 3 of the research implementation.

With five distinct subjects, the number of valid orders is 5! = 120.
Each permutation assigns one subject to each of the five examination positions,
with no subject omitted or repeated.
"""

from itertools import permutations
from typing import List, Tuple

from . import SUBJECTS


# Type alias for an examination schedule
Schedule = Tuple[str, ...]


def generate_all_schedules() -> List[Schedule]:
    """
    Generate all 120 valid examination schedules.

    Returns
    -------
    list of tuple
        Each tuple contains the five subject codes in examination order.
        Exactly 120 permutations are generated.

    Examples
    --------
    >>> schedules = generate_all_schedules()
    >>> len(schedules)
    120
    >>> all(len(s) == 5 for s in schedules)
    True
    >>> all(set(s) == set(SUBJECTS) for s in schedules)
    True
    """
    all_schedules = list(permutations(SUBJECTS))
    assert len(all_schedules) == 120, (
        f"Expected 120 permutations of 5 subjects, got {len(all_schedules)}"
    )
    return all_schedules


def schedule_to_string(schedule: Schedule, separator: str = " → ") -> str:
    """
    Format a schedule as a readable string.

    Parameters
    ----------
    schedule : tuple of str
        An examination schedule.
    separator : str
        Separator between subject codes.

    Returns
    -------
    str
        Human-readable schedule string.

    Examples
    --------
    >>> schedule_to_string(("M", "CS", "C", "E", "P"))
    'M → CS → C → E → P'
    """
    return separator.join(schedule)


def get_reversed_schedule(schedule: Schedule) -> Schedule:
    """
    Return the reversed examination order.

    The scoring formula S_r(π) = Σ D_{r,π_i} · D_{r,π_{i+1}} is symmetric
    under reversal: reversing a schedule produces an identical scheduling score.

    Parameters
    ----------
    schedule : tuple of str
        An examination schedule.

    Returns
    -------
    tuple of str
        The reversed schedule.
    """
    return tuple(reversed(schedule))


def validate_schedule(schedule: Schedule) -> bool:
    """
    Check that a schedule is a valid permutation of the five subjects.

    Parameters
    ----------
    schedule : tuple of str
        An examination schedule to validate.

    Returns
    -------
    bool
        True if the schedule contains exactly the five required subjects.
    """
    return set(schedule) == set(SUBJECTS) and len(schedule) == len(SUBJECTS)
