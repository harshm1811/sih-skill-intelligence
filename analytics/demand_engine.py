"""
Demand Intelligence Engine
Analyzes job postings to extract job-role demand, skill demand, and market trends.
"""

import pandas as pd
from typing import Dict, Any, List


def calculate_role_demand(jobs_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes aggregated demand metrics for each job role across Maharashtra.
    """
    roles = []
    grouped = jobs_df.groupby("role")

    for role_name, group in grouped:
        top_companies = group["company"].value_counts().head(5).to_dict()
        exp_dist = group["experience"].value_counts().to_dict()
        dist_dist = group["district"].value_counts().to_dict()

        roles.append({
            "role": role_name,
            "total_demand": int(len(group)),
            "average_salary": int(round(group["salary"].mean())),
            "min_salary": int(group["salary"].min()),
            "max_salary": int(group["salary"].max()),
            "experience_distribution": exp_dist,
            "district_distribution": dist_dist,
            "top_hiring_companies": top_companies
        })

    # Sort descending by total demand
    roles.sort(key=lambda x: x["total_demand"], reverse=True)

    return {
        "total_jobs_analyzed": int(len(jobs_df)),
        "unique_roles_count": len(roles),
        "roles": roles
    }


def calculate_district_role_demand(jobs_df: pd.DataFrame) -> Dict[str, List[Dict[str, Any]]]:
    """
    Computes role demand broken down by district.
    """
    district_roles = {}
    grouped = jobs_df.groupby(["district", "role"])

    for (district, role), group in grouped:
        if district not in district_roles:
            district_roles[district] = []
        district_roles[district].append({
            "role": role,
            "demand": int(len(group)),
            "average_salary": int(round(group["salary"].mean()))
        })

    # Sort each district's roles by demand descending
    for dist in district_roles:
        district_roles[dist].sort(key=lambda x: x["demand"], reverse=True)

    return district_roles


def calculate_skill_demand(
    jobs_df: pd.DataFrame,
    job_skills_df: pd.DataFrame,
    skills_df: pd.DataFrame = None
) -> Dict[str, Any]:
    """
    Computes demand for each skill at state and district levels.
    Joins job_skills with jobs to attribute geographic demand.
    """
    # Merge jobs with job_skills to get district per skill posting
    merged = job_skills_df.merge(
        jobs_df[["job_id", "district", "role", "salary"]],
        on="job_id",
        how="inner"
    )

    # Category lookup
    cat_map = {}
    desc_map = {}
    if skills_df is not None:
        for _, row in skills_df.iterrows():
            cat_map[row["skill_name"]] = row.get("category", "General")
            desc_map[row["skill_name"]] = row.get("description", "")

    # Statewide skill demand
    state_skills = []
    for skill_name, group in merged.groupby("skill"):
        prof_counts = group["proficiency"].value_counts().to_dict()
        dist_counts = group["district"].value_counts().to_dict()
        top_roles = group["role"].value_counts().head(3).to_dict()

        state_skills.append({
            "skill": skill_name,
            "category": cat_map.get(skill_name, "General"),
            "description": desc_map.get(skill_name, ""),
            "state_demand": int(len(group)),
            "proficiency_breakdown": prof_counts,
            "district_breakdown": dist_counts,
            "associated_roles": top_roles
        })

    state_skills.sort(key=lambda x: x["state_demand"], reverse=True)

    # District-level skill demand
    district_skills = {}
    for (district, skill_name), group in merged.groupby(["district", "skill"]):
        if district not in district_skills:
            district_skills[district] = {}
        district_skills[district][skill_name] = {
            "demand": int(len(group)),
            "category": cat_map.get(skill_name, "General"),
            "proficiency_breakdown": group["proficiency"].value_counts().to_dict()
        }

    return {
        "statewide_skills": state_skills,
        "district_skills": district_skills
    }

