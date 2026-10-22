# Reproducibility Guide

This guide describes how to reproduce every numerical finding, table, and figure reported in the manuscript:

> Khanna, T. (2026). *Comparative Analysis of Mathematically Optimized Examination Timetables Using Student–Teacher Difficulty Ratings: An A Level Exploratory Study*.

---

## 1. System Requirements

- **Python Version**: Python 3.9 or higher (tested on Python 3.12)
- **Supported Operating Systems**: Windows 10/11, macOS, Linux
- **Required Libraries**:
  - `pandas` (>= 1.5.0)
  - `numpy` (>= 1.24.0)
  - `matplotlib` (>= 3.7.0)
  - `PyYAML` (>= 6.0)
  - `pytest` (>= 7.0.0)

---

## 2. Quick Setup

```bash
# Clone the repository
git clone https://github.com/toshik-khanna/exam-scheduling-difficulty-analysis.git
cd exam-scheduling-difficulty-analysis

# Install dependencies
pip install -r requirements.txt
```

---

## 3. Running the Reproduction Pipeline

Execute the master experiment pipeline from the project root:

```bash
python experiments/run_analysis.py
```

### Generated Artifacts

The `results/` directories are recreated by the analysis. Generated files are excluded from Git history; their presence is not implied by a fresh clone.

Running this script automatically performs all computations and populates:

1. **`results/tables/`**:
   - `table_descriptive_statistics.csv`: Descriptive statistics (Mean, Median, Std, Min, Max) for Students, Teachers, and Combined groups (Table 8).
   - `table_group_optimization.csv`: Group baseline, selected, minimum scores, and reduction percentages.
   - `table_individual_results.csv`: Per-respondent optimization records (N=35).
   - `table_sensitivity_fairness.csv`: Equal weighting, minimax, and perturbation stability findings.

2. **`results/figures/`**:
   - `figure_1_sample_composition.png`: Figure 1 — Respondent composition.
   - `figure_2_computational_workflow.png`: Figure 2 — Computational workflow.
   - `figure_3_difficulty_means.png`: Figure 3 — Student, teacher and original assumed ratings.
   - `figure_4_mean_scheduling_scores.png`: Figure 4 — Mean scores for all 35 respondents.
   - `figure_5_score_reductions.png`: Figure 5 — Selected versus group-minimum reductions.
   - `figure_6_rating_distribution.png`: Figure 6 — Difficulty-rating frequency heatmap.
   - `figure_7_individual_optimality_gaps.png`: Figure 7 — Individual optimality-gap frequency histogram.

3. **`results/schedules/`**:
   - `all_120_schedules_ranked.csv`: Comprehensive score ranking for all 120 candidate examination schedules across Combined, Student, and Teacher cohorts.

---

## 4. Automated Testing and Verification

To execute the test suite (21 source-defined automated test functions) and verify all mathematical regression checkpoints:

```bash
pytest
# or: python run_tests.py
# or: pytest tests/ -v
```

### Verified Test Cases (24 tests across 7 modules):
- Exhaustive enumeration of $5! = 120$ permutations, 5 unique subjects, and reversal preservation (`test_permutations.py`, 3 tests)
- Consecutive-burden scoring, Khanna [1] assumed-score benchmarks (59 baseline, 45 minimum, 4 tied optima), and reversal symmetry (`test_scoring.py`, 4 tests)
- Input validation, duplicate rejection, rating range $[1, 5]$ bounds, and missing field rejection (`test_validation.py`, 4 tests)
- Individual optimizer structure and non-negative optimality gap ($G_r \ge 0$) (`test_individual_optimizer.py`, 2 tests)
- Group aggregation correctness and tie preservation (`test_group_optimizer.py`, 2 tests)
- Exact numerical reproducibility and sensitivity verification (`test_reproducibility.py`, 6 tests):
  - Respondent counts ($N=35$, 30 students, 5 teachers)
  - Descriptive subject means matching manuscript Table 8
  - Group baseline and minimum scores (Students 1,833/1,689; Teachers 294/273; Combined 2,127/1,963)
  - Combined optimal timetable count = 2
  - Teacher joint optimum divergence from student joint optimum
  - Exact rating perturbation sensitivity across 301 single-point scenarios (100% retention)


## Reproducibility safeguards

The fixed-sample run requires exactly 30 student and 5 teacher records and stops on missing records or failed numerical regression checkpoints. The YAML file is reference documentation and is not automatically loaded by the experiment script. Continuous integration is defined in `.github/workflows/reproduce.yml`; consult the workflow status for execution results. Survey-data reuse is separate from the MIT software license.


## Final manuscript chart alignment
The seven images generated from `python run_analysis.py` correspond **in order and statistical content** to Figures 1–7 of the accompanying manuscript. Captions are provided in the manuscript and should not be confused with chart titles. Generated files are not committed to Git and must be regenerated.
