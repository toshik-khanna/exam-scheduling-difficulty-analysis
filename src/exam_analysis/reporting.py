"""
Reporting Module
================

Generates and exports reproducible research tables and reports.

Component 8 of the research implementation.

Outputs include:
- Table 1 / Table 8: Descriptive statistics of difficulty ratings (CSV & text)
- Group-level comparison table (Baseline, Selected, Minimum, Reduction %)
- Individual-level optimization table (35 respondents)
- Complete ranking of all 120 schedules for each group
- Sensitivity and fairness summary
"""

import csv
import os
from typing import Dict, List, Tuple

from .individual_optimizer import IndividualResult
from .group_optimizer import GroupOptimizationResult
from .timetable_generator import schedule_to_string


def export_descriptive_statistics_csv(stats: Dict, output_filepath: str):
    """
    Export descriptive statistics to CSV.

    Columns: Subject, Group, N, Mean, Median, Std, Min, Max
    """
    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
    with open(output_filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Subject", "Group", "N", "Mean", "Median", "Std", "Min", "Max"])
        for group_key, group_name in [
            ("students", "Students"),
            ("teachers", "Teachers"),
            ("combined", "Combined"),
        ]:
            g_stats = stats.get(group_key, {})
            for subj, s in g_stats.items():
                writer.writerow([
                    subj,
                    group_name,
                    s["count"],
                    f"{s['mean']:.2f}",
                    f"{s['median']:.1f}",
                    f"{s['std']:.2f}",
                    s["min"],
                    s["max"],
                ])


def export_group_optimization_csv(
    group_results: Dict[str, GroupOptimizationResult],
    output_filepath: str,
):
    """
    Export group optimization summary to CSV.

    Columns: Group, N, Baseline, Previously_Selected, Minimum, Reduction_Pct, Optimal_Count
    """
    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
    with open(output_filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Group",
            "N",
            "Baseline_Score",
            "Khanna_Selected_Score",
            "Group_Minimum_Score",
            "Reduction_Pct",
            "Optimal_Schedule_Count",
        ])
        for key in ("students", "teachers", "combined"):
            res = group_results[key]
            writer.writerow([
                res.group_name,
                res.respondent_count,
                res.baseline_score,
                res.selected_score,
                res.minimum_score,
                f"{res.reduction_pct:.2f}",
                res.optimal_count,
            ])


def export_individual_results_csv(
    individual_results: List[IndividualResult],
    output_filepath: str,
):
    """
    Export all 35 respondent results to CSV.

    Columns: ID, Group, M, P, C, CS, E, Baseline, Selected, Minimum, Optimality_Gap, Reduction_Pct, Optimal_Count
    """
    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
    with open(output_filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "ID",
            "Group",
            "M",
            "P",
            "C",
            "CS",
            "E",
            "Baseline_Score",
            "Khanna_Selected_Score",
            "Individual_Minimum_Score",
            "Optimality_Gap",
            "Reduction_Pct",
            "Optimal_Schedule_Count",
        ])
        for r in individual_results:
            writer.writerow([
                r.respondent_id,
                r.group,
                r.ratings["M"],
                r.ratings["P"],
                r.ratings["C"],
                r.ratings["CS"],
                r.ratings["E"],
                r.baseline_score,
                r.selected_score,
                r.minimum_score,
                r.optimality_gap,
                f"{r.reduction_pct:.2f}",
                r.optimal_count,
            ])


def export_all_schedules_ranked_csv(
    group_results: Dict[str, GroupOptimizationResult],
    output_filepath: str,
):
    """
    Export all 120 schedules with ranks and scores for each group.
    """
    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)

    students_scores = group_results["students"].schedule_scores
    teachers_scores = group_results["teachers"].schedule_scores
    combined_scores = group_results["combined"].schedule_scores

    # Rank by combined score
    ranked_by_comb = sorted(combined_scores.items(), key=lambda x: x[1])

    with open(output_filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Rank_Combined",
            "Schedule",
            "Combined_Score",
            "Students_Score",
            "Teachers_Score",
        ])
        for rank, (sched, c_score) in enumerate(ranked_by_comb, start=1):
            writer.writerow([
                rank,
                schedule_to_string(sched),
                c_score,
                students_scores[sched],
                teachers_scores[sched],
            ])


def export_sensitivity_fairness_csv(
    equal_weighting: Dict,
    minimax: Dict,
    rating_sensitivity: Dict,
    optimality_gaps: Dict,
    output_filepath: str,
):
    """
    Export sensitivity and fairness analyses summary to CSV.
    """
    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
    with open(output_filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Metric", "Value", "Notes"])
        writer.writerow([
            "Equal_Weighting_Baseline",
            f"{equal_weighting['baseline_score']:.3f}",
            "0.5 * (mean_students + mean_teachers)",
        ])
        writer.writerow([
            "Equal_Weighting_Selected",
            f"{equal_weighting['selected_score']:.3f}",
            "Score for M->CS->C->E->P",
        ])
        writer.writerow([
            "Equal_Weighting_Minimum",
            f"{equal_weighting['minimum_score']:.3f}",
            "Minimum achievable under equal weighting",
        ])
        writer.writerow([
            "Equal_Weighting_Reduction_Pct",
            f"{equal_weighting['baseline_to_min_reduction_pct']:.2f}%",
            "Percentage reduction from baseline",
        ])
        writer.writerow([
            "Minimax_Lowest_Max_Burden",
            minimax["min_max_burden"],
            "Minimum worst-case respondent burden across all 120 schedules",
        ])
        writer.writerow([
            "Minimax_Optimal_Count",
            minimax["fair_count"],
            "Number of schedules achieving minimax value",
        ])
        writer.writerow([
            "Rating_Stability_Rate",
            f"{rating_sensitivity['stability_rate_pct']:.2f}%",
            rating_sensitivity.get(
                "summary_statement",
                f"{rating_sensitivity['stable_count']}/{rating_sensitivity['total_perturbations']} single-point perturbations leave original schedules optimal",
            ),
        ])
        writer.writerow([
            "Students_Mean_Optimality_Gap",
            optimality_gaps["students"]["mean"],
            f"Zero gap: {optimality_gaps['students']['zero_gap_pct']}% of students",
        ])
        writer.writerow([
            "Teachers_Mean_Optimality_Gap",
            optimality_gaps["teachers"]["mean"],
            f"Zero gap: {optimality_gaps['teachers']['zero_gap_pct']}% of teachers",
        ])
