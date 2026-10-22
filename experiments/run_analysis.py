"""
Main Experiment Script
======================

Executes the complete computational analysis and reproducibility pipeline for:
    "Comparative Analysis of Student and Teacher Difficulty Assessments in
     Mathematical Examination Timetabling: An Exploratory A Level Study"

Workflow:
1. Load and validate the 35 respondent records from CSV.
2. Compute descriptive statistics across subjects and groups.
3. Enumerate all 120 valid examination permutations.
4. Evaluate consecutive-burden scores across 4,200 respondent-timetable pairs.
5. Identify individual optima, tie counts, and optimality gaps.
6. Identify group-level optima for Students, Teachers, and Combined populations.
7. Execute sensitivity, equal-weighting, minimax fairness, and stability tests.
8. Validate regression assertions against published findings.
9. Export CSV tables to results/tables/ and schedule rankings to results/schedules/.
10. Generate publication figures to results/figures/.
"""

import os
import sys

# Configure UTF-8 encoding for standard output on Windows
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Ensure repository root is on sys.path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

SRC_PATH = os.path.join(REPO_ROOT, "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from exam_analysis.data_loader import load_ratings, split_by_group
from exam_analysis.validation import validate_records
from exam_analysis.statistics import comparative_statistics, format_statistics_table
from exam_analysis.timetable_generator import generate_all_schedules, schedule_to_string
from exam_analysis.individual_optimizer import (
    optimize_all_individuals,
    format_individual_summary,
)
from exam_analysis.group_optimizer import optimize_all_groups
from exam_analysis.sensitivity import (
    evaluate_equal_group_weighting,
    evaluate_minimax_fairness,
    evaluate_rating_sensitivity,
    compare_optimality_gaps,
)
from exam_analysis.reporting import (
    export_descriptive_statistics_csv,
    export_group_optimization_csv,
    export_individual_results_csv,
    export_all_schedules_ranked_csv,
    export_sensitivity_fairness_csv,
)
from exam_analysis.visualization import generate_all_figures


def run_pipeline(
    data_path: str = "data/survey/difficulty_ratings.csv",
    tables_dir: str = "results/tables",
    figures_dir: str = "results/figures",
    schedules_dir: str = "results/schedules",
):
    """Execute complete analysis pipeline."""
    print("=" * 75)
    print("EXAM SCHEDULING DIFFICULTY ANALYSIS — REPRODUCIBILITY PIPELINE")
    print("=" * 75)

    # 1. Load Data
    full_data_path = os.path.join(REPO_ROOT, data_path)
    print(f"\n[1/7] Loading dataset from: {full_data_path}")
    records = load_ratings(full_data_path)
    print(f"      Loaded {len(records)} records successfully.")

    # 2. Validate Data
    print("\n[2/7] Validating data integrity...")
    val_report = validate_records(records, strict_counts=True)
    print(val_report.summary())
    if not val_report.is_valid:
        raise ValueError("Data validation failed! See errors above.")

    students, teachers = split_by_group(records)

    # 3. Descriptive Statistics
    print("\n[3/7] Calculating descriptive statistics...")
    stats = comparative_statistics(students, teachers)
    for g_key, g_name in [("students", "Students (30)"), ("teachers", "Teachers (5)"), ("combined", "Combined (35)")]:
        print(format_statistics_table(stats[g_key], g_name))

    # 4. Timetable Generation & Scoring
    print("\n[4/7] Generating 120 examination permutations & evaluating individual scores...")
    all_schedules = generate_all_schedules()
    print(f"      Total unique examination permutations: {len(all_schedules)}")
    print(f"      Total respondent-timetable score evaluations: {len(records) * len(all_schedules):,}")

    individual_results = optimize_all_individuals(records)
    print(format_individual_summary(individual_results))

    # 5. Group Optimization
    print("\n[5/7] Performing group-level optimization...")
    group_results = optimize_all_groups(records, all_schedules)

    for g_key in ("students", "teachers", "combined"):
        res = group_results[g_key]
        print(f"\n{'-' * 50}")
        print(res.summary())

    # Regression Checks
    print("\n" + "=" * 50)
    print("REGRESSION INTEGRITY CHECKS")
    print("=" * 50)
    s_res = group_results["students"]
    t_res = group_results["teachers"]
    c_res = group_results["combined"]

    checks = [
        ("Student baseline score == 1833", s_res.baseline_score == 1833),
        ("Student minimum score == 1689", s_res.minimum_score == 1689),
        ("Teacher baseline score == 294", t_res.baseline_score == 294),
        ("Teacher selected score == 274", t_res.selected_score == 274),
        ("Teacher minimum score == 273", t_res.minimum_score == 273),
        ("Combined baseline score == 2127", c_res.baseline_score == 2127),
        ("Combined minimum score == 1963", c_res.minimum_score == 1963),
        ("Combined optimal timetable count == 2", c_res.optimal_count == 2),
    ]

    all_passed = True
    for desc, passed in checks:
        status = "PASSED" if passed else "FAILED"
        print(f"  [{status}] {desc}")
        if not passed:
            all_passed = False

    if not all_passed:
        raise RuntimeError("Numerical regression checks failed; refusing to report successful reproduction.")
    else:
        print("\nAll regression checks PASSED with exact numerical precision.")

    # 6. Sensitivity and Fairness Analysis
    print("\n[6/7] Running sensitivity and fairness extensions...")
    equal_weighting = evaluate_equal_group_weighting(students, teachers, all_schedules)
    minimax = evaluate_minimax_fairness(records, all_schedules)
    rating_sensitivity = evaluate_rating_sensitivity(records)
    optimality_gaps = compare_optimality_gaps(individual_results)

    print(f"      Equal-group weighting baseline: {equal_weighting['baseline_score']:.2f}")
    print(f"      Equal-group weighting minimum:  {equal_weighting['minimum_score']:.2f}")
    print(f"      Minimax minimum peak burden:    {minimax['min_max_burden']}")
    print(f"      Rating perturbation stability:  {rating_sensitivity['stability_rate_pct']:.2f}%")
    print(f"      Sensitivity finding:            {rating_sensitivity['summary_statement']}")
    print(f"      Students mean optimality gap:   {optimality_gaps['students']['mean']:.2f}")
    print(f"      Teachers mean optimality gap:   {optimality_gaps['teachers']['mean']:.2f}")

    # 7. Export Tables and Generate Figures
    print("\n[7/7] Exporting tables, schedules, and publication figures...")
    out_tables = os.path.join(REPO_ROOT, tables_dir)
    out_figures = os.path.join(REPO_ROOT, figures_dir)
    out_schedules = os.path.join(REPO_ROOT, schedules_dir)

    export_descriptive_statistics_csv(stats, os.path.join(out_tables, "table_descriptive_statistics.csv"))
    export_group_optimization_csv(group_results, os.path.join(out_tables, "table_group_optimization.csv"))
    export_individual_results_csv(individual_results, os.path.join(out_tables, "table_individual_results.csv"))
    export_all_schedules_ranked_csv(group_results, os.path.join(out_schedules, "all_120_schedules_ranked.csv"))
    export_sensitivity_fairness_csv(
        equal_weighting,
        minimax,
        rating_sensitivity,
        optimality_gaps,
        os.path.join(out_tables, "table_sensitivity_fairness.csv"),
    )
    print(f"      Exported tables to: {out_tables}")
    print(f"      Exported schedules to: {out_schedules}")

    generated_figs = generate_all_figures(stats, group_results, individual_results, out_figures)
    print(f"      Generated {len(generated_figs)} figures in: {out_figures}")
    for fig_path in generated_figs:
        print(f"        - {os.path.basename(fig_path)}")

    print("\n" + "=" * 75)
    print("ANALYSIS COMPLETE — NUMERICAL REGRESSION CHECKS PASSED")
    print("=" * 75)


if __name__ == "__main__":
    run_pipeline()
