"""
Exam Scheduling Difficulty Analysis
====================================

A Python implementation for comparative analysis of student and teacher
difficulty assessments in mathematical examination timetabling.

This package implements the consecutive-subject burden scoring model from
Khanna [1] and extends it to 35 respondent-specific difficulty rating vectors,
enabling comparison between student and teacher optimal examination schedules.

References
----------
[1] Khanna, T. (2025). Optimizing Examination Timetables Using Mathematical
    Scoring Models.
"""

__version__ = "1.0.0"
__author__ = "Toshik Khanna"

# Subject codes used throughout the analysis
SUBJECTS = ("M", "P", "C", "CS", "E")

# Full subject names for display purposes
SUBJECT_NAMES = {
    "M": "Mathematics",
    "P": "Physics",
    "C": "Chemistry",
    "CS": "Computer Science",
    "E": "English",
}

# Reference examination schedules
BASELINE_SCHEDULE = ("M", "P", "C", "E", "CS")
KHANNA_SELECTED_SCHEDULE = ("M", "CS", "C", "E", "P")

# Original assumed difficulty scores from Khanna [1]
ORIGINAL_ASSUMED_SCORES = {
    "M": 5,
    "P": 5,
    "C": 4,
    "CS": 3,
    "E": 2,
}
