# Relationship to Prior Research

## Context and Foundation: Khanna [1]

In the preliminary study:

> Khanna, T. (2025). *Optimizing Examination Timetables Using Mathematical Scoring Models*. DOI: 10.5281/zenodo.23512498

the consecutive-subject burden model was introduced and solved for an assumed set of difficulty scores:

- Mathematics: 5
- Physics: 5
- Chemistry: 4
- Computer Science: 3
- English: 2

Under this single rating vector, the baseline examination order:

$$\pi_{\text{baseline}} = (\text{M}, \text{P}, \text{C}, \text{E}, \text{CS})$$

yielded a score of **59**, while the selected optimal schedule:

$$\pi_{\text{selected}} = (\text{M}, \text{CS}, \text{C}, \text{E}, \text{P})$$

achieved the minimum score of **45** (a 23.73% reduction). Exactly 4 tied schedules achieved this minimum due to reversal and internal symmetry.

---

## Contribution of the Present Study (Paper 02)

The current paper:

> Khanna, T. (2026). *Comparative Analysis of Student and Teacher Difficulty Assessments in Mathematical Examination Timetabling: An Exploratory A Level Study*.

advances the research by moving from **assumed, uniform difficulty weights** to **empirical difficulty assessments** collected from 35 participants (30 students and 5 teachers).

### Key Differences and Advancements

| Dimension | Khanna [1] | Present Study (Paper 02) |
|---|---|---|
| **Difficulty Input** | 1 assumed static vector | 35 empirical individual vectors (30 students, 5 teachers) |
| **Data Source** | Theoretical assumption | Anonymized survey rating records |
| **Search Space** | 120 schedules evaluated once | 4,200 schedule evaluations (120 × 35) |
| **Optima Analyzed** | Single assumed optimum | Individual optima, Student group optimum, Teacher group optimum, Combined optimum |
| **Stakeholder Comparison** | None | Systematic contrast between student and teacher optima |
| **Fairness & Sensitivity** | Not evaluated | Equal-group weighting, minimax fairness, perturbation robustness |

### Stakeholder Divergence

A critical empirical finding revealed by this implementation is that the **students' joint optimum** and **teachers' joint optimum** diverge:

- **Students & Combined joint optimum**: $\text{M} \to \text{CS} \to \text{C} \to \text{E} \to \text{P}$ (score: 1,689 for students, 1,963 combined).
- **Teachers joint optimum**: $\text{M} \to \text{C} \to \text{CS} \to \text{E} \to \text{P}$ (score: 273 for teachers, where the Khanna selected schedule scores 274).

This divergence illustrates the practical importance of empirical stakeholder evaluation in educational optimization models.
