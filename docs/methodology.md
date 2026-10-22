# Computational Methodology

## Mathematical Model

This study implements and evaluates the consecutive-subject examination scheduling model defined in Khanna [1]:

$$S_r(\pi) = \sum_{i=1}^{4} D_{r,\pi_i} \cdot D_{r,\pi_{i+1}}$$

where:
- $r \in \{1, \dots, 35\}$ indexes the survey respondents (30 students $S01$–$S30$ and 5 teachers $T01$–$T05$).
- $\pi = (\pi_1, \pi_2, \pi_3, \pi_4, \pi_5)$ denotes a permutation of the five subjects $\mathcal{S} = \{\text{Mathematics (M)}, \text{Physics (P)}, \text{Chemistry (C)}, \text{Computer Science (CS)}, \text{English (E)}\}$.
- $D_{r,s} \in \{1, 2, 3, 4, 5\}$ denotes respondent $r$'s perceived difficulty rating for subject $s$.
- $\pi_i$ is the subject assigned to examination slot $i$.

### Reversal Symmetry

The objective function exhibits exact reversal symmetry. For any permutation $\pi = (\pi_1, \pi_2, \pi_3, \pi_4, \pi_5)$ and its reversal $\pi^{\text{rev}} = (\pi_5, \pi_4, \pi_3, \pi_2, \pi_1)$:

$$S_r(\pi^{\text{rev}}) = \sum_{i=1}^{4} D_{r,\pi_{5-(i-1)}} \cdot D_{r,\pi_{5-i}} = \sum_{j=1}^{4} D_{r,\pi_{j+1}} \cdot D_{r,\pi_j} = S_r(\pi)$$

Consequently, every optimal timetable is accompanied by an equally optimal reverse schedule.

---

## Computational Algorithm

Given $|\mathcal{S}| = 5$, the total search space consists of:

$$5! = 120 \text{ candidate timetables}$$

Because this search space is small and discrete, the algorithm employs **exhaustive permutation enumeration** via Python's standard library `itertools.permutations`. No approximations, metaheuristics, genetic algorithms, or neural networks are required.

The computational procedure evaluates:

$$120 \text{ permutations} \times 35 \text{ respondents} = 4,200 \text{ score evaluations}$$

### Group-Level Aggregation

The aggregate score of timetable $\pi$ for group $G$ is defined as:

$$S_G(\pi) = \sum_{r \in G} S_r(\pi)$$

The group-optimal timetable $\pi_G^*$ solves:

$$\pi_G^* = \arg\min_{\pi \in \Pi} S_G(\pi)$$

where $\Pi$ denotes the set of all 120 candidate permutations.

---

## Analytical Extensions

### 1. Equal-Group Weighting

To account for the numerical imbalance between student records ($N_S = 30$) and teacher records ($N_T = 5$), an equal-group objective is evaluated:

$$S_{\text{equal}}(\pi) = \frac{1}{2} \left( \frac{S_{\text{students}}(\pi)}{30} + \frac{S_{\text{teachers}}(\pi)}{5} \right)$$

This equalizes the aggregate influence of each stakeholder category.

### 2. Individual Optimality Gap

For each respondent $r$, the optimality gap $G_r$ relative to the selected timetable $\pi_{\text{selected}} = (\text{M}, \text{CS}, \text{C}, \text{E}, \text{P})$ is defined as:

$$G_r = S_r(\pi_{\text{selected}}) - S_r^*$$

where $S_r^* = \min_{\pi \in \Pi} S_r(\pi)$ is respondent $r$'s individual global minimum score.

### 3. Minimax Fairness

To evaluate whether aggregate minimization disadvantages specific individuals, a minimax objective evaluates:

$$M(\pi) = \max_{r \in R} S_r(\pi)$$

and identifies the schedule minimizing the maximum burden imposed on any single participant.

### 4. Rating Perturbation Sensitivity

The stability of the optimal schedules is evaluated under all valid single-point perturbations ($\pm 1$ within $[1, 5]$) across each respondent's subject ratings. Across 301 valid single-point perturbations of individual difficulty ratings, the two original aggregate-optimal schedules remained optimal in every case. In six perturbations, additional schedules also attained the minimum score.
