"""
Data Ingestion and Validation Module
Loads and validates the 8 representative datasets from data/
"""

import os
import pandas as pd
from typing import Dict, Any
from .config import DATA_DIR


REQUIRED_FILES = {
    "districts": "districts.csv",
    "skills": "skills.csv",
    "jobs": "jobs.csv",
    "job_skills": "job_skills.csv",
    "courses": "courses.csv",
    "course_skills": "course_skills.csv",
    "employers": "employers.csv",
    "placements": "placements.csv"
}

REQUIRED_COLUMNS = {
    "districts": ["district_id", "district_name", "region"],
    "skills": ["skill_id", "skill_name", "category"],
    "jobs": ["job_id", "district", "company", "role", "salary", "experience", "description", "date"],
    "job_skills": ["job_id", "skill", "proficiency"],
    "courses": ["course_id", "course_name", "district", "capacity", "completion_rate", "placement_rate"],
    "course_skills": ["course_id", "skill", "proficiency"],
    "employers": ["company_id", "company_name", "industry_sector", "district"],
    "placements": ["placement_id", "course_id", "student_id", "company_name", "role", "salary_offered", "district"]
}


def load_all_data(data_dir=None) -> Dict[str, pd.DataFrame]:
    """
    Loads all 8 CSV datasets into a structured dictionary of pandas DataFrames.
    """
    directory = data_dir or DATA_DIR
    dfs = {}
    for key, filename in REQUIRED_FILES.items():
        file_path = os.path.join(directory, filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Required dataset file not found: {file_path}")
        dfs[key] = pd.read_csv(file_path)
    return dfs


def validate_dataset(dfs: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    """
    Validates structural and relational integrity of the loaded datasets.
    """
    report = {
        "status": "PASS",
        "file_counts": {},
        "integrity_checks": {},
        "issues": []
    }

    # Check required columns
    for key, req_cols in REQUIRED_COLUMNS.items():
        df = dfs.get(key)
        if df is None:
            report["status"] = "FAIL"
            report["issues"].append(f"Missing DataFrame for '{key}'")
            continue

        report["file_counts"][key] = len(df)
        missing_cols = [col for col in req_cols if col not in df.columns]
        if missing_cols:
            report["status"] = "FAIL"
            report["issues"].append(f"{key}.csv missing required columns: {missing_cols}")

    # Check referential integrity
    # 1. job_skills -> jobs
    missing_job_ids = set(dfs["job_skills"]["job_id"]) - set(dfs["jobs"]["job_id"])
    if missing_job_ids:
        report["status"] = "FAIL"
        report["issues"].append(f"{len(missing_job_ids)} job_skills referencing nonexistent jobs")
    else:
        report["integrity_checks"]["job_skills_foreign_keys"] = "PASS"

    # 2. course_skills -> courses
    missing_course_ids = set(dfs["course_skills"]["course_id"]) - set(dfs["courses"]["course_id"])
    if missing_course_ids:
        report["status"] = "FAIL"
        report["issues"].append(f"{len(missing_course_ids)} course_skills referencing nonexistent courses")
    else:
        report["integrity_checks"]["course_skills_foreign_keys"] = "PASS"

    # 3. placements -> courses
    missing_placement_courses = set(dfs["placements"]["course_id"]) - set(dfs["courses"]["course_id"])
    if missing_placement_courses:
        report["status"] = "FAIL"
        report["issues"].append(f"{len(missing_placement_courses)} placements referencing nonexistent courses")
    else:
        report["integrity_checks"]["placements_foreign_keys"] = "PASS"

    return report

