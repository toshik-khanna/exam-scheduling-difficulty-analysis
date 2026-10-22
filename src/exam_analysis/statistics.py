"""
Statistics Module
=================

Calculates descriptive statistics for the difficulty rating data.

Component 2 of the research implementation.

Computes means, medians, standard deviations, minimum/maximum ratings,
and frequency distributions for each subject across student, teacher,
and combined populations.
"""

from typing import Dict, List, Tuple
import math


def calculate_mean(values: List[int]) -> float:
    """Calculate arithmetic mean."""
    if not values:
        raise ValueError("Cannot calculate mean of empty list")
    return sum(values) / len(values)


def calculate_median(values: List[int]) -> float:
    """Calculate median value."""
    if not values:
        raise ValueError("Cannot calculate median of empty list")
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    if n % 2 == 0:
        return (sorted_vals[n // 2 - 1] + sorted_vals[n // 2]) / 2
    return float(sorted_vals[n // 2])


def calculate_std(values: List[int], ddof: int = 1) -> float:
    """
    Calculate sample standard deviation.

    Parameters
    ----------
    values : list of int
        Data values.
    ddof : int
        Delta degrees of freedom. Default is 1 (sample std).

    Returns
    -------
    float
        Standard deviation.
    """
    if len(values) < 2:
        return 0.0
    mean = calculate_mean(values)
    variance = sum((x - mean) ** 2 for x in values) / (len(values) - ddof)
    return math.sqrt(variance)


def rating_frequency(values: List[int], min_rating: int = 1, max_rating: int = 5) -> Dict[int, int]:
    """
    Count the frequency of each rating value.

    Parameters
    ----------
    values : list of int
        Rating values.
    min_rating : int
        Minimum rating in the scale.
    max_rating : int
        Maximum rating in the scale.

    Returns
    -------
    dict
        Mapping from rating value to count.
    """
    freq = {r: 0 for r in range(min_rating, max_rating + 1)}
    for v in values:
        freq[v] = freq.get(v, 0) + 1
    return freq


def subject_statistics(records: List[Dict], subjects: Tuple[str, ...] = ("M", "P", "C", "CS", "E")) -> Dict:
    """
    Calculate comprehensive descriptive statistics for each subject.

    Parameters
    ----------
    records : list of dict
        Respondent records.
    subjects : tuple of str
        Subject codes.

    Returns
    -------
    dict
        Nested dict: subject -> {mean, median, std, min, max, count, frequencies}
    """
    stats = {}
    for subj in subjects:
        values = [r[subj] for r in records]
        stats[subj] = {
            "mean": round(calculate_mean(values), 2),
            "median": calculate_median(values),
            "std": round(calculate_std(values), 2),
            "min": min(values),
            "max": max(values),
            "count": len(values),
            "sum": sum(values),
            "frequencies": rating_frequency(values),
        }
    return stats


def comparative_statistics(
    students: List[Dict],
    teachers: List[Dict],
    subjects: Tuple[str, ...] = ("M", "P", "C", "CS", "E"),
) -> Dict:
    """
    Calculate and compare statistics across student, teacher, and combined groups.

    Parameters
    ----------
    students : list of dict
        Student records.
    teachers : list of dict
        Teacher records.
    subjects : tuple of str
        Subject codes.

    Returns
    -------
    dict
        Keys: 'students', 'teachers', 'combined', each containing subject statistics.
    """
    combined = students + teachers
    return {
        "students": subject_statistics(students, subjects),
        "teachers": subject_statistics(teachers, subjects),
        "combined": subject_statistics(combined, subjects),
    }


def format_statistics_table(stats: Dict, group_name: str) -> str:
    """
    Format statistics as a readable text table.

    Parameters
    ----------
    stats : dict
        Output of subject_statistics().
    group_name : str
        Name of the respondent group.

    Returns
    -------
    str
        Formatted table string.
    """
    header = f"\nDescriptive Statistics — {group_name}"
    sep = "=" * 70
    col_header = f"{'Subject':<15} {'Mean':>6} {'Median':>7} {'Std':>6} {'Min':>5} {'Max':>5} {'N':>5}"
    lines = [header, sep, col_header, "-" * 70]

    for subj, s in stats.items():
        lines.append(
            f"{subj:<15} {s['mean']:>6.2f} {s['median']:>7.1f} "
            f"{s['std']:>6.2f} {s['min']:>5d} {s['max']:>5d} {s['count']:>5d}"
        )

    lines.append(sep)
    return "\n".join(lines)
