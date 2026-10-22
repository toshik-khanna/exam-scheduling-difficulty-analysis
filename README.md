# Exam Scheduling Difficulty Analysis

**Comparative Analysis of Mathematically Optimized Examination Timetables Using Student–Teacher Difficulty Ratings: An A Level Exploratory Study**

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests: pytest](https://img.shields.io/badge/Tests-pytest-orange.svg)](tests/)

---

## Overview

This repository provides a complete, reproducible Python research implementation for:

> Khanna, T. (2026). *Comparative Analysis of Mathematically Optimized Examination Timetables Using Student–Teacher Difficulty Ratings: An A Level Exploratory Study*.

The implementation extends the foundational examination scheduling optimization from Khanna [1]—which optimized for a single assumed difficulty vector—to **35 respondent-specific empirical difficulty rating vectors** (30 A Level students and 5 teachers), demonstrating how stakeholder perceptions affect optimal timetable selection.

---

## Mathematical Model

The consecutive-subject burden objective evaluates an examination order $\pi$ for respondent $r$:

$$S_r(\pi) = \sum_{i=1}^{4} D_{r,\pi_i} \cdot D_{r,\pi_{i+1}}$$

where:
- $r \in \{1, \dots, 35\}$ indexes survey respondents ($S01$–$S30$ students, $T01$–$T05$ teachers).
- $\pi$ is an examination order permutation of the five subjects: Mathematics (M), Physics (P), Chemistry (C), Computer Science (CS), and English (E).
- $D_{r,s} \in \{1, 2, 3, 4, 5\}$ denotes respondent $r$'s difficulty rating for subject $s$.

---

## Verified Research Results

All findings reproduce the accompanying manuscript values with exact precision:

| Cohort | N | Baseline Score | Khanna [1] Selected | Group Minimum | Reduction (%) | Joint Optimal Schedule |
|---|:---:|:---:|:---:|:---:|:---:|---|
| **Students** | 30 | **1,833** | **1,689** | **1,689** | **7.86%** | `M → CS → C → E → P` (+ reversal) |
| **Teachers** | 5 | **294** | **274** | **273** | **7.14%** | `M → C → CS → E → P` (+ reversal) |
| **Combined** | 35 | **2,127** | **1,963** | **1,963** | **7.71%** | `M → CS → C → E → P` (+ reversal) |

### Key Findings
1. **Divergent Optima**: Students' joint optimum (`M → CS → C → E → P`, score 1,689) and teachers' joint optimum (`M → C → CS → E → P`, score 273) diverge. The Khanna selected schedule scores 274 for teachers.
2. **Reversal Symmetry**: All optimal schedules possess an equally optimal reverse permutation due to commutative consecutive-pair products.
3. **Robustness**: Across 301 valid single-point perturbations of individual difficulty ratings, the two original aggregate-optimal schedules remained optimal in every case. In six perturbations, additional schedules also attained the minimum score.

---

## Quick Start

### Installation

```bash
git clone https://github.com/toshik-khanna/exam-scheduling-difficulty-analysis.git
cd exam-scheduling-difficulty-analysis
pip install -r requirements.txt
```

### Run Full Analysis Pipeline

```bash
python experiments/run_analysis.py
# or simply:
python run_analysis.py
```

This validates the dataset, calculates descriptive statistics, evaluates all 4,200 respondent–timetable scores, checks regression benchmarks, and populates:
- `results/tables/`: CSV summary tables
- `results/figures/`: Publication-quality figures (Figures 1–7) at 300 DPI
- `results/schedules/`: Complete ranking of all 120 candidate schedules

### Run Automated Tests

```bash
pytest
# or: python run_tests.py
# or: pytest tests/ -v
```

All 21 regression and unit tests execute and pass across the 6 test modules:
- Permutation enumeration and uniqueness (3 tests)
- Consecutive-burden scoring and reversal symmetry (4 tests)
- Input validation and bounds checking (4 tests)
- Individual optimization and optimality gaps (2 tests)
- Group aggregation and symmetry preservation (2 tests)
- Numerical reproducibility and perturbation sensitivity (6 tests)

---

## Repository Structure

```
exam-scheduling-difficulty-analysis/
├── README.md                          # Repository documentation
├── requirements.txt                   # Project dependencies
├── pyproject.toml                     # Package and pytest configuration
├── run_tests.py                       # Test-suite launcher
├── LICENSE                            # MIT License
├── CITATION.cff                       # Citation metadata
├── .gitignore                         # Git exclusion rules
├── run_analysis.py                    # Root execution forwarder
├── config/
│   └── experiment.yaml                # Configuration parameters & reference baselines
├── data/
│   ├── README.md                      # Data provenance & ethical considerations
│   └── survey/
│       └── difficulty_ratings.csv     # 35 anonymized survey records (30 students, 5 teachers)
├── src/
│   └── exam_analysis/
│       ├── __init__.py                # Package initialization & constants
│       ├── data_loader.py             # CSV loading & group splitting
│       ├── validation.py              # Data integrity & validation reporting
│       ├── statistics.py              # Descriptive statistics & distributions
│       ├── timetable_generator.py     # 5! = 120 permutation enumeration & reversals
│       ├── scoring.py                 # Mathematical objective scoring
│       ├── individual_optimizer.py    # Per-respondent optimization & optimality gaps
│       ├── group_optimizer.py         # Group-level aggregate optimization
│       ├── sensitivity.py             # Equal-weighting, minimax fairness, & sensitivity
│       ├── visualization.py           # Publication-quality figures (300 DPI)
│       └── reporting.py               # CSV export of tables & schedule rankings
├── experiments/
│   └── run_analysis.py                # Main experiment reproducibility script
├── results/
│   ├── tables/                        # Exported CSV tables
│   ├── figures/                       # Publication figures (Figures 1–7)
│   └── schedules/                     # Ranked schedule CSVs
├── .github/workflows/reproduce.yml  # GitHub Actions verification
├── tests/
│   ├── test_permutations.py           # Permutation enumeration & uniqueness
│   ├── test_scoring.py                # Objective scoring & Khanna [1] benchmarks
│   ├── test_validation.py             # Input integrity & boundary testing
│   ├── test_individual_optimizer.py   # Individual optimization & optimality gaps
│   ├── test_group_optimizer.py        # Group-level aggregation & symmetries
│   └── test_reproducibility.py        # Exact numerical regression verification
└── docs/
    ├── methodology.md                 # Detailed mathematical methodology & proofs
    ├── reproducibility.md             # Reproducibility verification guide
    └── research_relationship.md       # Comparative analysis with Khanna [1]
```

---


**Reproduction notice:** Contents of `results/` are generated by the pipeline and ignored by Git; re-run the analysis to recreate tables and plots. Survey data are not automatically covered by the software MIT license; confirm the right to publish and reuse individual ratings.

## References

[1] Khanna, T. (2026). *Optimizing Examination Scheduling Using Mathematical Optimization Techniques: An A Level Mathematical Investigation*. DOI: [10.5281/zenodo.23512498](https://doi.org/10.5281/zenodo.23512498).

---

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.


## Reproducibility safeguards

The production pipeline rejects incomplete respondent counts and raises an error when any numerical regression checkpoint fails. `config/experiment.yaml` is a **reference configuration**, not a runtime-loaded parameter source; the current pipeline uses the documented paths and benchmark constants in the Python code. GitHub Actions runs pytest and the analysis on supported Python versions. A green CI status is required before citing tests as passing. The MIT license applies to software; survey-data reuse requires separate permission.
