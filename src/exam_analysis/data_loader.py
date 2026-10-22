"""
Data Loader Module
==================

Reads the anonymized difficulty rating records from CSV input.

Component 1 of the research implementation.

Expected CSV format:
    ID,M,P,C,CS,E

Where:
    - ID: Respondent identifier (S01-S30 for students, T01-T05 for teachers)
    - M, P, C, CS, E: Integer difficulty ratings (1-5) for each subject
"""

import csv
import os
from typing import Dict, List, Tuple


def load_ratings(filepath: str) -> List[Dict]:
    """
    Load difficulty ratings from a CSV file.

    Parameters
    ----------
    filepath : str
        Path to the CSV file containing difficulty ratings.

    Returns
    -------
    list of dict
        Each dict contains:
        - 'ID': str, respondent identifier
        - 'group': str, 'student' or 'teacher'
        - 'M', 'P', 'C', 'CS', 'E': int, difficulty ratings

    Raises
    ------
    FileNotFoundError
        If the input file does not exist.
    ValueError
        If required columns are missing or data format is invalid.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Input file not found: {filepath}")

    records = []
    required_columns = {"ID", "M", "P", "C", "CS", "E"}

    with open(filepath, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        # Validate columns
        if reader.fieldnames is None:
            raise ValueError("CSV file appears to be empty")

        actual_columns = set(reader.fieldnames)
        missing = required_columns - actual_columns
        if missing:
            raise ValueError(f"Missing required CSV columns: {missing}")

        for line_num, row in enumerate(reader, start=2):
            respondent_id = row["ID"].strip()

            # Determine group from ID prefix
            if respondent_id.startswith("S") and respondent_id[1:].isdigit():
                group = "student"
            elif respondent_id.startswith("T") and respondent_id[1:].isdigit():
                group = "teacher"
            else:
                raise ValueError(
                    f"Line {line_num}: Invalid respondent ID '{respondent_id}'. "
                    f"Expected format S01-S30 or T01-T05."
                )

            # Parse ratings
            ratings = {}
            for subject in ("M", "P", "C", "CS", "E"):
                raw_value = row[subject].strip()
                if not raw_value:
                    raise ValueError(
                        f"Line {line_num}: Missing rating for subject '{subject}' "
                        f"(respondent {respondent_id})"
                    )
                try:
                    value = int(raw_value)
                except ValueError:
                    raise ValueError(
                        f"Line {line_num}: Non-integer rating '{raw_value}' "
                        f"for subject '{subject}' (respondent {respondent_id})"
                    )
                ratings[subject] = value

            record = {"ID": respondent_id, "group": group, **ratings}
            records.append(record)

    return records


def split_by_group(records: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
    """
    Split records into student and teacher groups.

    Parameters
    ----------
    records : list of dict
        All respondent records.

    Returns
    -------
    tuple of (list, list)
        (students, teachers)
    """
    students = [r for r in records if r["group"] == "student"]
    teachers = [r for r in records if r["group"] == "teacher"]
    return students, teachers


def get_ratings_vector(record: Dict) -> Dict[str, int]:
    """
    Extract the five-subject difficulty rating vector from a record.

    Parameters
    ----------
    record : dict
        A respondent record.

    Returns
    -------
    dict
        Mapping from subject code to integer rating.
    """
    return {subj: record[subj] for subj in ("M", "P", "C", "CS", "E")}
