"""
Visualization Module
====================

Generates publication-quality figures reproducing all manuscript figures:

Figure 1: Student and teacher sample composition
Figure 2: Mean difficulty ratings by group
Figure 3: Scheduling scores across groups (Baseline, Khanna selected, Minimum)
Figure 4: Percentage score reductions across groups
Figure 5: Distribution of subject difficulty ratings
Figure 6: Computational optimization workflow diagram
Figure 7: Individual optimality gaps across respondents

Uses the paper's restrained color palette:
    - Navy:       #1B2A4A (Baseline / Primary)
    - Teal:       #2A9D8F (Optimized results)
    - Dark Teal:  #264653 (Students)
    - Coral:      #E76F51 (Teachers)
    - Sand/Gold:  #E9C46A (Combined)
    - Grey:       #808080 (Supporting / Neutral)
"""

import os
from typing import Dict, List
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

from .individual_optimizer import IndividualResult
from .group_optimizer import GroupOptimizationResult
from . import SUBJECTS, SUBJECT_NAMES


# Publication color palette
NAVY = "#1B2A4A"
TEAL = "#2A9D8F"
DARK_TEAL = "#264653"
CORAL = "#E76F51"
GOLD = "#E9C46A"
GREY = "#808080"
LIGHT_GREY = "#E0E0E0"


def setup_plot_style():
    """Apply consistent academic typography and clean layout."""
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.size": 11,
        "axes.labelsize": 12,
        "axes.titlesize": 13,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "figure.titlesize": 14,
        "figure.dpi": 300,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.3,
        "grid.linestyle": "--",
    })


def plot_sample_composition(
    n_students: int = 30,
    n_teachers: int = 5,
    output_dir: str = "results/figures",
) -> str:
    """
    Figure 1: Student and teacher sample composition.
    """
    setup_plot_style()
    os.makedirs(output_dir, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6, 5))

    groups = ["Students", "Teachers"]
    counts = [n_students, n_teachers]
    colors = [DARK_TEAL, CORAL]

    bars = ax.bar(groups, counts, color=colors, width=0.5, edgecolor="none", zorder=3)

    for bar, count in zip(bars, counts):
        pct = (count / (n_students + n_teachers)) * 100
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.8,
            f"N = {count}\n({pct:.1f}%)",
            ha="center",
            va="bottom",
            fontweight="bold",
            color=NAVY,
        )

    ax.set_ylabel("Number of Respondents")
    ax.set_ylim(0, 36)
    ax.set_title("Figure 1. Respondent Sample Composition\n(N = 35 total respondents)", pad=15)

    filepath = os.path.join(output_dir, "figure_1_sample_composition.png")
    fig.tight_layout()
    fig.savefig(filepath, dpi=300)
    plt.close(fig)
    return filepath


def plot_difficulty_means(
    stats: Dict,
    output_dir: str = "results/figures",
) -> str:
    """
    Figure 2: Mean difficulty ratings by group across subjects.
    """
    setup_plot_style()
    os.makedirs(output_dir, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8.5, 5))

    x = np.arange(len(SUBJECTS))
    width = 0.25

    student_means = [stats["students"][s]["mean"] for s in SUBJECTS]
    teacher_means = [stats["teachers"][s]["mean"] for s in SUBJECTS]
    combined_means = [stats["combined"][s]["mean"] for s in SUBJECTS]

    b1 = ax.bar(x - width, student_means, width, label="Students (N=30)", color=DARK_TEAL, zorder=3)
    b2 = ax.bar(x, teacher_means, width, label="Teachers (N=5)", color=CORAL, zorder=3)
    b3 = ax.bar(x + width, combined_means, width, label="Combined (N=35)", color=TEAL, zorder=3)

    # Add value annotations
    for bars in (b1, b2, b3):
        for bar in bars:
            h = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                h + 0.05,
                f"{h:.2f}",
                ha="center",
                va="bottom",
                fontsize=8,
                rotation=0,
            )

    ax.set_xticks(x)
    ax.set_xticklabels([f"{SUBJECT_NAMES[s]}\n({s})" for s in SUBJECTS])
    ax.set_ylabel("Mean Subject Difficulty Rating (1–5)")
    ax.set_ylim(0, 5.5)
    ax.legend(frameon=True, loc="upper right")
    ax.set_title("Figure 2. Mean Subject Difficulty Ratings Across Respondent Groups", pad=15)

    filepath = os.path.join(output_dir, "figure_2_difficulty_means.png")
    fig.tight_layout()
    fig.savefig(filepath, dpi=300)
    plt.close(fig)
    return filepath


def plot_aggregate_scores(
    group_results: Dict[str, GroupOptimizationResult],
    output_dir: str = "results/figures",
) -> str:
    """
    Figure 3: Aggregate scheduling scores across groups (Baseline, Khanna selected, Minimum).
    """
    setup_plot_style()
    os.makedirs(output_dir, exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5), gridspec_kw={"width_ratios": [1, 2]})

    # Left plot: Teachers (smaller scale)
    t_res = group_results["teachers"]
    labels_t = ["Baseline", "Khanna [1]\nSelected", "Group\nMinimum"]
    scores_t = [t_res.baseline_score, t_res.selected_score, t_res.minimum_score]
    colors_t = [NAVY, GREY, TEAL]

    bars_t = ax1.bar(labels_t, scores_t, color=colors_t, width=0.55, zorder=3)
    for bar, val in zip(bars_t, scores_t):
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 4,
            f"{val:,}",
            ha="center",
            fontweight="bold",
            fontsize=9,
        )
    ax1.set_ylabel("Total Scheduling Score S_G(π)")
    ax1.set_ylim(0, 340)
    ax1.set_title("Teachers (N = 5)")

    # Right plot: Students and Combined
    groups = ["Students (N=30)", "Combined (N=35)"]
    x = np.arange(len(groups))
    width = 0.25

    baselines = [group_results["students"].baseline_score, group_results["combined"].baseline_score]
    selecteds = [group_results["students"].selected_score, group_results["combined"].selected_score]
    minimums = [group_results["students"].minimum_score, group_results["combined"].minimum_score]

    b1 = ax2.bar(x - width, baselines, width, label="Baseline", color=NAVY, zorder=3)
    b2 = ax2.bar(x, selecteds, width, label="Khanna [1] Selected", color=GREY, zorder=3)
    b3 = ax2.bar(x + width, minimums, width, label="Group Minimum", color=TEAL, zorder=3)

    for bars in (b1, b2, b3):
        for bar in bars:
            h = bar.get_height()
            ax2.text(
                bar.get_x() + bar.get_width() / 2,
                h + 25,
                f"{int(h):,}",
                ha="center",
                fontweight="bold",
                fontsize=9,
            )

    ax2.set_xticks(x)
    ax2.set_xticklabels(groups)
    ax2.set_ylim(0, 2400)
    ax2.legend(frameon=True, loc="upper left")
    ax2.set_title("Students & Combined Sample")

    fig.suptitle("Figure 3. Comparison of Aggregate Examination Scheduling Scores", y=1.02)
    filepath = os.path.join(output_dir, "figure_3_aggregate_scores.png")
    fig.tight_layout()
    fig.savefig(filepath, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return filepath


def plot_score_reductions(
    group_results: Dict[str, GroupOptimizationResult],
    output_dir: str = "results/figures",
) -> str:
    """
    Figure 4: Percentage score reductions from baseline to minimum.
    """
    setup_plot_style()
    os.makedirs(output_dir, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7, 4.5))

    groups = ["Students (30)", "Teachers (5)", "Combined (35)"]
    reductions = [
        group_results["students"].reduction_pct,
        group_results["teachers"].reduction_pct,
        group_results["combined"].reduction_pct,
    ]
    colors = [DARK_TEAL, CORAL, TEAL]

    bars = ax.bar(groups, reductions, color=colors, width=0.45, zorder=3)

    for bar, red in zip(bars, reductions):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.2,
            f"{red:.2f}%",
            ha="center",
            va="bottom",
            fontweight="bold",
            color=NAVY,
        )

    ax.set_ylabel("Burden Reduction from Baseline (%)")
    ax.set_ylim(0, 10.0)
    ax.set_title("Figure 4. Model-Defined Consecutive Burden Reduction by Group", pad=15)

    filepath = os.path.join(output_dir, "figure_4_score_reductions.png")
    fig.tight_layout()
    fig.savefig(filepath, dpi=300)
    plt.close(fig)
    return filepath


def plot_rating_distribution(
    stats: Dict,
    output_dir: str = "results/figures",
) -> str:
    """
    Figure 5: Distribution of subject difficulty ratings (1 to 5).
    """
    setup_plot_style()
    os.makedirs(output_dir, exist_ok=True)
    fig, ax = plt.subplots(figsize=(9, 5))

    rating_vals = [1, 2, 3, 4, 5]
    n_ratings = len(rating_vals)
    n_subjects = len(SUBJECTS)
    x = np.arange(n_subjects)
    width = 0.15

    palette = ["#90E0EF", "#48CAE4", "#0096C7", "#023E8A", "#03045E"]

    for i, r_val in enumerate(rating_vals):
        counts = [stats["combined"][subj]["frequencies"].get(r_val, 0) for subj in SUBJECTS]
        ax.bar(
            x + (i - 2) * width,
            counts,
            width,
            label=f"Rating {r_val}",
            color=palette[i],
            zorder=3,
        )

    ax.set_xticks(x)
    ax.set_xticklabels([f"{SUBJECT_NAMES[s]}\n({s})" for s in SUBJECTS])
    ax.set_ylabel("Respondent Count (N = 35)")
    ax.set_ylim(0, 30)
    ax.legend(title="Rating", frameon=True, loc="upper left")
    ax.set_title("Figure 5. Frequency Distribution of Subject Difficulty Ratings", pad=15)

    filepath = os.path.join(output_dir, "figure_5_rating_distribution.png")
    fig.tight_layout()
    fig.savefig(filepath, dpi=300)
    plt.close(fig)
    return filepath


def generate_workflow_diagram(output_dir: str = "results/figures") -> str:
    """
    Figure 6: Computational optimization workflow diagram.
    """
    setup_plot_style()
    os.makedirs(output_dir, exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis("off")

    # Workflow steps as stylized flowchart boxes
    boxes = [
        ("Step 1: Survey Data Ingestion\n35 records: 30 students + 5 teachers\n5-point difficulty ratings", 0.15, 0.75),
        ("Step 2: Data Validation\nRange check [1-5], unique IDs\nNo missing data replacement", 0.50, 0.75),
        ("Step 3: Descriptive Analysis\nMeans, medians, standard deviations\nFrequency distributions", 0.85, 0.75),
        ("Step 4: Permutation Enumeration\n5! = 120 valid examination orders\nExhaustive generation", 0.15, 0.35),
        ("Step 5: Mathematical Scoring\n4,200 score evaluations (120 × 35)\nS_r(π) = Σ D_{r,π_i} · D_{r,π_{i+1}}", 0.50, 0.35),
        ("Step 6: Optimization & Reporting\nGroup & individual optima\nSensitivity & reproducibility tests", 0.85, 0.35),
    ]

    bbox_props = dict(boxstyle="round,pad=0.6", facecolor="#EBF4F6", edgecolor=TEAL, lw=1.5)

    for text, px, py in boxes:
        ax.text(
            px,
            py,
            text,
            ha="center",
            va="center",
            fontsize=9.5,
            bbox=bbox_props,
            color=NAVY,
            weight="semibold",
        )

    # Connecting arrows
    arrow_props = dict(arrowstyle="->", lw=2, color=NAVY)
    ax.annotate("", xy=(0.35, 0.75), xytext=(0.28, 0.75), arrowprops=arrow_props)
    ax.annotate("", xy=(0.70, 0.75), xytext=(0.63, 0.75), arrowprops=arrow_props)
    ax.annotate("", xy=(0.15, 0.50), xytext=(0.15, 0.62), arrowprops=arrow_props)
    ax.annotate("", xy=(0.35, 0.35), xytext=(0.28, 0.35), arrowprops=arrow_props)
    ax.annotate("", xy=(0.70, 0.35), xytext=(0.63, 0.35), arrowprops=arrow_props)

    ax.set_title("Figure 6. Python Computational Workflow for Examination Timetable Optimization", pad=20, fontsize=12, fontweight="bold")
    ax.set_xlim(0, 1)
    ax.set_ylim(0.1, 1.0)

    filepath = os.path.join(output_dir, "figure_6_computational_workflow.png")
    fig.tight_layout()
    fig.savefig(filepath, dpi=300)
    plt.close(fig)
    return filepath


def plot_individual_gaps(
    individual_results: List[IndividualResult],
    output_dir: str = "results/figures",
) -> str:
    """
    Figure 7: Individual optimality gaps across all 35 respondents.
    G_r = S_r(π_selected) - S_r*
    """
    setup_plot_style()
    os.makedirs(output_dir, exist_ok=True)
    fig, ax = plt.subplots(figsize=(11, 4.5))

    ids = [r.respondent_id for r in individual_results]
    gaps = [r.optimality_gap for r in individual_results]
    colors = [DARK_TEAL if r.group == "student" else CORAL for r in individual_results]

    x = np.arange(len(ids))
    bars = ax.bar(x, gaps, color=colors, width=0.6, zorder=3)

    for bar, gap in zip(bars, gaps):
        if gap > 0:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.1,
                str(gap),
                ha="center",
                va="bottom",
                fontsize=8,
                fontweight="bold",
            )

    ax.set_xticks(x)
    ax.set_xticklabels(ids, rotation=90, fontsize=8)
    ax.set_ylabel("Optimality Gap G_r = S_r(π_sel) - S_r*")
    ax.set_ylim(0, max(gaps) + 2 if max(gaps) > 0 else 5)

    # Custom legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=DARK_TEAL, label="Students (S01–S30)"),
        Patch(facecolor=CORAL, label="Teachers (T01–T05)"),
    ]
    ax.legend(handles=legend_elements, frameon=True, loc="upper right")
    ax.set_title(
        "Figure 7. Individual Optimality Gaps Relative to Khanna [1] Selected Timetable\n(0 indicates selected schedule is individually optimal)",
        pad=15,
    )

    filepath = os.path.join(output_dir, "figure_7_individual_optimality_gaps.png")
    fig.tight_layout()
    fig.savefig(filepath, dpi=300)
    plt.close(fig)
    return filepath


def generate_all_figures(
    stats: Dict,
    group_results: Dict[str, GroupOptimizationResult],
    individual_results: List[IndividualResult],
    output_dir: str = "results/figures",
) -> List[str]:
    """Generate and save all 7 publication figures."""
    figures = [
        plot_sample_composition(30, 5, output_dir),
        plot_difficulty_means(stats, output_dir),
        plot_aggregate_scores(group_results, output_dir),
        plot_score_reductions(group_results, output_dir),
        plot_rating_distribution(stats, output_dir),
        generate_workflow_diagram(output_dir),
        plot_individual_gaps(individual_results, output_dir),
    ]
    return figures
