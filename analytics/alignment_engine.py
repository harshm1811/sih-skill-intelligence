"""
Course Alignment and Effectiveness Engine
Assesses how well course curricula match local industry skill demands,
evaluates completion & placement effectiveness, and identifies curriculum gaps.
"""

import pandas as pd
from typing import Dict, Any, List


def evaluate_course_alignment(
    courses_df: pd.DataFrame,
    course_skills_df: pd.DataFrame,
    demand_data: Dict[str, Any],
    gap_data: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Evaluates curriculum alignment, effectiveness score, and modernization recommendations
    for all vocational courses.
    """
    district_skills = demand_data["district_skills"]
    district_gaps = gap_data["district_gaps"]

    # Map course -> list of skills taught with proficiency
    course_skills_map = {}
    for _, row in course_skills_df.iterrows():
        cid = row["course_id"]
        if cid not in course_skills_map:
            course_skills_map[cid] = []
        course_skills_map[cid].append({
            "skill": row["skill"],
            "proficiency": row["proficiency"]
        })

    aligned_courses = []

    for _, row in courses_df.iterrows():
        cid = row["course_id"]
        cname = row["course_name"]
        district = row["district"]
        capacity = int(row["capacity"])
        comp_rate = float(row["completion_rate"])
        place_rate = float(row["placement_rate"])

        # Core throughput metrics
        completed = int(round(capacity * comp_rate))
        placed = int(round(completed * place_rate))
        effectiveness = round(comp_rate * place_rate, 4)

        taught_skills = course_skills_map.get(cid, [])
        taught_skill_names = [s["skill"] for s in taught_skills]

        # Local district demand for these taught skills
        dist_demands = district_skills.get(district, {})
        avg_dist_demand = 50.0  # Normalized baseline reference

        matched_skills = []
        alignment_points = 0.0

        for s_info in taught_skills:
            s_name = s_info["skill"]
            local_demand = dist_demands.get(s_name, {}).get("demand", 0)
            matched_skills.append({
                "skill": s_name,
                "proficiency_taught": s_info["proficiency"],
                "district_demand": local_demand
            })
            # Add alignment weight
            alignment_points += min(1.0, local_demand / avg_dist_demand)

        # Alignment Score (0 - 100)
        if taught_skills:
            alignment_score = round((alignment_points / len(taught_skills)) * 100, 1)
        else:
            alignment_score = 0.0

        # Identify missing critical/high skills in this district not taught by the course
        dist_gap_list = district_gaps.get(district, [])
        critical_unmet = [
            g["skill"] for g in dist_gap_list
            if g["priority"] in ["CRITICAL", "HIGH"] and g["skill"] not in taught_skill_names
        ][:3]  # Top 3 modernization targets

        # Actionable recommendations
        recommendations = []
        if effectiveness >= 0.65 and alignment_score >= 60.0:
            recommendations.append(
                f"High-performing aligned program: Recommend capacity expansion (+25-50 seats) in {district}."
            )
        elif effectiveness < 0.50:
            recommendations.append(
                f"Needs performance intervention: Placement rate ({int(place_rate*100)}%) requires industry mentorship."
            )

        if critical_unmet:
            recommendations.append(
                f"Curriculum Modernization: Integrate high-demand local skills: {', '.join(critical_unmet)}."
            )

        aligned_courses.append({
            "course_id": cid,
            "course_name": cname,
            "district": district,
            "capacity": capacity,
            "completion_rate": round(comp_rate, 2),
            "placement_rate": round(place_rate, 2),
            "completed_trainees": completed,
            "placed_trainees": placed,
            "effectiveness_score": effectiveness,
            "alignment_score": alignment_score,
            "skills_count": len(taught_skills),
            "skills_taught": matched_skills,
            "missing_critical_skills": critical_unmet,
            "action_recommendations": recommendations
        })

    # Sort descending by effectiveness score
    aligned_courses.sort(key=lambda x: x["effectiveness_score"], reverse=True)
    return aligned_courses

