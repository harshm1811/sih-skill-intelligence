"""
Training Supply Engine
Evaluates vocational courses, student throughput, and skill training coverage.
"""

import pandas as pd
from typing import Dict, Any, List


def calculate_course_metrics(courses_df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Computes completed trainees, placed trainees, and effectiveness scores per course.
    """
    courses_metrics = []

    for _, row in courses_df.iterrows():
        cid = row["course_id"]
        cname = row["course_name"]
        district = row["district"]
        capacity = int(row["capacity"])
        comp_rate = float(row["completion_rate"])
        place_rate = float(row["placement_rate"])

        # Completed trainees = round(capacity * completion_rate)
        completed = int(round(capacity * comp_rate))
        # Placed trainees = round(completed * placement_rate)
        placed = int(round(completed * place_rate))

        # Overall course effectiveness = completion_rate * placement_rate
        # Represents the fraction of enrolled capacity successfully trained and placed
        effectiveness = round(comp_rate * place_rate, 4)

        if effectiveness >= 0.65:
            eff_tier = "High Performing"
        elif effectiveness >= 0.50:
            eff_tier = "Moderate"
        else:
            eff_tier = "Needs Improvement"

        courses_metrics.append({
            "course_id": cid,
            "course_name": cname,
            "district": district,
            "capacity": capacity,
            "completion_rate": round(comp_rate, 2),
            "placement_rate": round(place_rate, 2),
            "completed_trainees": completed,
            "placed_trainees": placed,
            "effectiveness_score": effectiveness,
            "effectiveness_tier": eff_tier
        })

    return courses_metrics


def calculate_skill_training_coverage(
    courses_df: pd.DataFrame,
    course_skills_df: pd.DataFrame
) -> Dict[str, Any]:
    """
    Calculates training coverage (annual completers) for each skill at district and state levels.
    """
    # Merge course skills with course metadata to link capacity & district
    merged = course_skills_df.merge(
        courses_df[["course_id", "course_name", "district", "capacity", "completion_rate"]],
        on="course_id",
        how="inner"
    )

    # Compute completed trainees per course entry
    merged["completers"] = (merged["capacity"] * merged["completion_rate"]).round().astype(int)

    # District-level skill coverage
    district_coverage = {}
    for (district, skill), group in merged.groupby(["district", "skill"]):
        if district not in district_coverage:
            district_coverage[district] = {}
        total_cov = int(group["completers"].sum())
        courses_teaching = group[["course_id", "course_name", "completers"]].to_dict("records")
        district_coverage[district][skill] = {
            "training_coverage": total_cov,
            "courses_teaching": courses_teaching
        }

    # Statewide skill coverage
    state_coverage = {}
    for skill, group in merged.groupby("skill"):
        total_cov = int(group["completers"].sum())
        dist_breakdown = group.groupby("district")["completers"].sum().to_dict()
        state_coverage[skill] = {
            "state_training_coverage": total_cov,
            "district_breakdown": {d: int(c) for d, c in dist_breakdown.items()}
        }

    return {
        "district_coverage": district_coverage,
        "state_coverage": state_coverage
    }

