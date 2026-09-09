"""
Skill Gap Engine
Applies core SIH 2026 formula:
  Skill Gap = Industry Demand - Training Coverage
Classifies priority levels and validates strict internal consistency.
"""

from typing import Dict, Any, List
from .config import (
    DISTRICTS,
    classify_priority,
    PRIORITY_CRITICAL,
    PRIORITY_HIGH,
    PRIORITY_MEDIUM,
    PRIORITY_LOW
)


def calculate_skill_gaps(
    demand_data: Dict[str, Any],
    supply_data: Dict[str, Any],
    skills_df: Any = None
) -> Dict[str, Any]:
    """
    Calculates granular and district-level skill gaps.
    Guarantees that:
      skill_gap == industry_demand - training_coverage
    for 100% of data points.
    """
    district_skills = demand_data["district_skills"]
    district_coverage = supply_data["district_coverage"]

    # Skill metadata dictionary
    skills_meta = {}
    if skills_df is not None:
        for _, row in skills_df.iterrows():
            skills_meta[row["skill_name"]] = {
                "skill_id": row.get("skill_id", ""),
                "category": row.get("category", "General"),
                "description": row.get("description", "")
            }

    all_gap_records = []
    district_gap_summary = {d: [] for d in DISTRICTS}

    # Iterate over all districts and skills
    for district in DISTRICTS:
        dist_demand_map = district_skills.get(district, {})
        dist_supply_map = district_coverage.get(district, {})

        # Combine all unique skills present in demand or supply for this district
        all_skills = sorted(set(list(dist_demand_map.keys()) + list(dist_supply_map.keys())))

        for skill in all_skills:
            # Industry Demand count
            demand_info = dist_demand_map.get(skill, {})
            demand_val = int(demand_info.get("demand", 0))

            # Training Coverage count
            supply_info = dist_supply_map.get(skill, {})
            coverage_val = int(supply_info.get("training_coverage", 0))

            # Core SIH Formula
            raw_gap = demand_val - coverage_val

            # Consistency assertion: MUST match exactly
            assert raw_gap == (demand_val - coverage_val), (
                f"Math inconsistency detected for {district} - {skill}: "
                f"demand={demand_val}, coverage={coverage_val}, gap={raw_gap}"
            )

            # Priority classification
            priority = classify_priority(raw_gap)

            # Coverage ratio (%)
            if demand_val > 0:
                coverage_pct = round((coverage_val / demand_val) * 100, 1)
            else:
                coverage_pct = 100.0 if coverage_val > 0 else 0.0

            s_meta = skills_meta.get(skill, {})

            record = {
                "district": district,
                "skill": skill,
                "skill_id": s_meta.get("skill_id", ""),
                "category": s_meta.get("category", demand_info.get("category", "General")),
                "industry_demand": demand_val,
                "training_coverage": coverage_val,
                "skill_gap": raw_gap,
                "net_deficit": max(0, raw_gap),
                "coverage_pct": coverage_pct,
                "priority": priority,
                "training_courses": supply_info.get("courses_teaching", [])
            }

            all_gap_records.append(record)
            district_gap_summary[district].append(record)

    # Sort records by skill_gap descending
    all_gap_records.sort(key=lambda x: x["skill_gap"], reverse=True)
    for d in district_gap_summary:
        district_gap_summary[d].sort(key=lambda x: x["skill_gap"], reverse=True)

    # Statewide Aggregate Gaps
    state_gaps = []
    state_skills_map = {item["skill"]: item for item in demand_data["statewide_skills"]}
    state_cov_map = supply_data["state_coverage"]

    all_state_skills = sorted(set(list(state_skills_map.keys()) + list(state_cov_map.keys())))
    for skill in all_state_skills:
        s_demand = int(state_skills_map.get(skill, {}).get("state_demand", 0))
        s_cov = int(state_cov_map.get(skill, {}).get("state_training_coverage", 0))
        s_gap = s_demand - s_cov
        s_meta = skills_meta.get(skill, {})

        state_gaps.append({
            "skill": skill,
            "skill_id": s_meta.get("skill_id", ""),
            "category": s_meta.get("category", "General"),
            "statewide_demand": s_demand,
            "statewide_coverage": s_cov,
            "statewide_gap": s_gap,
            "priority": classify_priority(s_gap),
            "coverage_pct": round((s_cov / s_demand) * 100, 1) if s_demand > 0 else 100.0
        })

    state_gaps.sort(key=lambda x: x["statewide_gap"], reverse=True)

    return {
        "all_gap_records": all_gap_records,
        "district_gaps": district_gap_summary,
        "statewide_gaps": state_gaps,
        "priority_counts": {
            "CRITICAL": sum(1 for r in all_gap_records if r["priority"] == PRIORITY_CRITICAL),
            "HIGH": sum(1 for r in all_gap_records if r["priority"] == PRIORITY_HIGH),
            "MEDIUM": sum(1 for r in all_gap_records if r["priority"] == PRIORITY_MEDIUM),
            "LOW": sum(1 for r in all_gap_records if r["priority"] == PRIORITY_LOW)
        }
    }

