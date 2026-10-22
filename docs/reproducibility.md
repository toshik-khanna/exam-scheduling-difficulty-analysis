# Reproducibility Guide

This guide describes how to reproduce every numerical finding, table, and figure reported in the manuscript:

> Khanna, T. (2025). *Comparative Analysis of Student and Teacher Difficulty Assessments in Mathematical Examination Timetabling: An Exploratory A Level Study*.

---

## 1. System Requirements

- **Python Version**: Python 3.9 or higher (tested on Python 3.12)
- **Supported Operating Systems**: Windows 10/11, macOS, Linux
- **Required Libraries**:
  - `pandas` (>= 1.5.0)
  - `numpy` (>= 1.23.0)
  - `matplotlib` (>= 3.6.0)
  - `PyYAML` (>= 6.0)
  - `pytest` (>= 7.0.0)

---

## 2. Quick Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/exam-scheduling-difficulty-analysis.git
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

Running this script automatically performs all computations and populates:

1. **`results/tables/`**:
   - `table_descriptive_statistics.csv`: Descriptive statistics (Mean, Median, Std, Min, Max) for Students, Teachers, and Combined groups (Table 8).
   - `table_group_optimization.csv`: Group baseline, selected, minimum scores, and reduction percentages.
   - `table_individual_results.csv`: Per-respondent optimization records (N=35).
   - `table_sensitivity_fairness.csv`: Equal weighting, minimax, and perturbation stability findings.

2. **`results/figures/`**:
   - `figure_1_sample_composition.png`: Sample composition (Figure 1).
   - `figure_2_difficulty_means.png`: Mean difficulty comparisons (Figure 2).
   - `figure_3_aggregate_scores.png`: Aggregate scheduling scores (Figure 3).
   - `figure_4_score_reductions.png`: Percentage score reductions (Figure 4).
   - `figure_5_rating_distribution.png`: Rating distribution frequencies (Figure 5).
   - `figure_6_computational_workflow.png`: Optimization workflow diagram (Figure 6).
   - `figure_7_individual_optimality_gaps.png`: Individual optimality gaps (Figure 7).

3. **`results/schedules/`**:
   - `all_120_schedules_ranked.csv`: Comprehensive score ranking for all 120 candidate examination schedules across Combined, Student, and Teacher cohorts.

---

## 4. Automated Testing and Verification

To execute the test suite and verify all mathematical regression checkpoints:

```bash
pytest tests/ -v
```

### Verified Test Cases:
- Exhaustive enumeration of $5! = 120$ permutations (`test_permutations.py`)
- Reversal symmetry of consecutive-burden objective across all schedules (`test_scoring.py`)
- Original Khanna [1] assumed-score regression checkpoints (59 baseline, 45 minimum) (`test_scoring.py`)
- Input validation and bounds checking (`test_validation.py`)
- Individual optimizer gap non-negativity (`test_individual_optimizer.py`)
- Group aggregation correctness and tie preservation (`test_group_optimizer.py`)
- Exact numerical reproducibility of all manuscript findings (`test_reproducibility.py`):
  - Students baseline = 1,833; minimum = 1,689
  - Teachers baseline = 294; minimum = 273
  - Combined baseline = 2,127; minimum = 1,963
  - Combined optimal timetable count = 2
