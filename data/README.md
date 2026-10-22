# Data Documentation

## Survey Data

### File: `survey/difficulty_ratings.csv`

Contains anonymized subject-difficulty ratings from 35 respondents (30 students and 5 teachers) for five A Level subjects.

### Columns

| Column | Description | Type | Range |
|--------|-------------|------|-------|
| ID | Anonymized respondent identifier | String | S01–S30 (students), T01–T05 (teachers) |
| M | Mathematics difficulty rating | Integer | 1–5 |
| P | Physics difficulty rating | Integer | 1–5 |
| C | Chemistry difficulty rating | Integer | 1–5 |
| CS | Computer Science difficulty rating | Integer | 1–5 |
| E | English difficulty rating | Integer | 1–5 |

### Rating Scale

- 1 = Least difficult
- 5 = Most difficult

### Respondent Groups

- **Students (S01–S30):** 30 A Level students
- **Teachers (T01–T05):** 5 A Level teachers

### Data Integrity

- All ratings are integers in [1, 5]
- All respondent IDs are unique
- No missing values
- Data has not been modified to produce desired mathematical results

### Ethical Considerations

- All respondents are anonymized
- Participation procedures and release permission require confirmation from the researcher's retained survey documentation
- Software MIT licensing does not by itself license the individual survey responses. Confirm rights and applicable consent requirements before redistribution.
