"""
Analytics Pipeline Orchestrator
Executes the full data flow:
  Industry Data -> Skill Extraction -> Demand Intelligence -> Skill Gap ->
  Course Alignment -> Recommendations -> District Training Plan
Exports clean, validated JSON files for backend consumption.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any

from .config import (
    OUTPUT_DIR,
    PROBLEM_STATEMENT_ID,
    PROJECT_NAME,
    PROTOTYPE_VERSION,
    DATASET_DISCLAIMER,
    DISTRICTS
)
from .loader import load_all_data, validate_dataset
from .demand_engine import (
    calculate_role_demand,
    calculate_district_role_demand,
    calculate_skill_demand
)
from .supply_engine import (
    calculate_course_metrics,
    calculate_skill_training_coverage
)
from .gap_engine import calculate_skill_gaps
from .alignment_engine import evaluate_course_alignment
from .district_planner import generate_district_training_plans


def build_metadata() -> Dict[str, Any]:
    """Generates standard metadata header for all output JSONs."""
    return {
        "problem_statement_id": PROBLEM_STATEMENT_ID,
        "project_name": PROJECT_NAME,
        "prototype_version": PROTOTYPE_VERSION,
        "representative_sample_data": True,
        "disclaimer": DATASET_DISCLAIMER,
        "generated_at": datetime.now(timezone.utc).isoformat()
    }


def run_pipeline() -> Dict[str, Any]:
    """
    Runs the complete analytics pipeline, validates mathematical consistency,
    and writes the 5 output JSON files.
    """
    print("[1/6] Ingesting and validating datasets...")
    dfs = load_all_data()
    val_report = validate_dataset(dfs)
    if val_report["status"] != "PASS":
        raise ValueError(f"Dataset validation failed: {val_report['issues']}")
    print(f"      Passed. Loaded {len(dfs)} datasets without errors.")

    print("[2/6] Computing Demand Intelligence...")
    role_demand = calculate_role_demand(dfs["jobs"])
    dist_role_demand = calculate_district_role_demand(dfs["jobs"])
    skill_demand = calculate_skill_demand(dfs["jobs"], dfs["job_skills"], dfs["skills"])
    print(f"      Analyzed {role_demand['total_jobs_analyzed']} job postings across {role_demand['unique_roles_count']} roles.")

    print("[3/6] Computing Training Supply & Capacity...")
    course_metrics = calculate_course_metrics(dfs["courses"])
    skill_coverage = calculate_skill_training_coverage(dfs["courses"], dfs["course_skills"])
    print(f"      Evaluated {len(course_metrics)} training courses.")

    print("[4/6] Executing Skill Gap Engine (Demand - Coverage)...")
    gap_data = calculate_skill_gaps(skill_demand, skill_coverage, dfs["skills"])
    print(f"      Generated {len(gap_data['all_gap_records'])} district-skill gap calculations.")
    print(f"      Priority counts: {gap_data['priority_counts']}")

    print("[5/6] Evaluating Course Alignment & Effectiveness...")
    aligned_courses = evaluate_course_alignment(
        dfs["courses"],
        dfs["course_skills"],
        skill_demand,
        gap_data
    )
    print(f"      Evaluated curriculum alignment and effectiveness for {len(aligned_courses)} courses.")

    print("[6/6] Generating District Training Plans...")
    training_plans = generate_district_training_plans(
        dfs["districts"],
        gap_data,
        dfs["courses"],
        aligned_courses
    )
    print(f"      Created training plans for {len(DISTRICTS)} districts.")

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    meta = build_metadata()

    # 1. dashboard.json
    total_jobs = len(dfs["jobs"])
    total_capacity = int(dfs["courses"]["capacity"].sum())
    total_completers = sum(c["completed_trainees"] for c in course_metrics)
    total_placements = sum(c["placed_trainees"] for c in course_metrics)

    district_cards = []
    for d in DISTRICTS:
        d_jobs = len(dfs["jobs"][dfs["jobs"]["district"] == d])
        d_courses = len(dfs["courses"][dfs["courses"]["district"] == d])
        d_cap = int(dfs["courses"][dfs["courses"]["district"] == d]["capacity"].sum())
        d_gaps = gap_data["district_gaps"].get(d, [])
        crit_count = sum(1 for g in d_gaps if g["priority"] == "CRITICAL")
        high_count = sum(1 for g in d_gaps if g["priority"] == "HIGH")

        district_cards.append({
            "district": d,
            "jobs_count": d_jobs,
            "courses_count": d_courses,
            "training_capacity": d_cap,
            "critical_gaps": crit_count,
            "high_gaps": high_count
        })

    dashboard_json = {
        "metadata": meta,
        "kpis": {
            "total_job_postings": total_jobs,
            "total_training_courses": len(dfs["courses"]),
            "total_enrolled_capacity": total_capacity,
            "total_annual_completers": total_completers,
            "total_annual_placements": total_placements,
            "overall_placement_rate": round(total_placements / total_completers, 2) if total_completers else 0.0,
            "critical_skill_gaps": gap_data["priority_counts"]["CRITICAL"],
            "high_skill_gaps": gap_data["priority_counts"]["HIGH"]
        },
        "top_statewide_demanded_roles": role_demand["roles"][:6],
        "top_statewide_critical_skills": gap_data["statewide_gaps"][:8],
        "district_summaries": district_cards
    }
    with open(OUTPUT_DIR / "dashboard.json", "w", encoding="utf-8") as f:
        json.dump(dashboard_json, f, indent=2)

    # 2. district_analysis.json
    districts_analysis_json = {
        "metadata": meta,
        "districts": {}
    }
    dist_meta_map = {r["district_name"]: r for _, r in dfs["districts"].iterrows()}

    for d in DISTRICTS:
        d_info = dist_meta_map.get(d, {})
        d_jobs_df = dfs["jobs"][dfs["jobs"]["district"] == d]
        d_gaps = gap_data["district_gaps"].get(d, [])

        districts_analysis_json["districts"][d] = {
            "district_id": d_info.get("district_id", ""),
            "district_name": d,
            "region": d_info.get("region", ""),
            "industrial_focus": d_info.get("industrial_focus", ""),
            "total_job_demand": len(d_jobs_df),
            "average_salary": int(round(d_jobs_df["salary"].mean())) if len(d_jobs_df) else 0,
            "top_hiring_companies": d_jobs_df["company"].value_counts().head(5).to_dict(),
            "top_roles": dist_role_demand.get(d, [])[:5],
            "skills_analysis": {
                "critical_gaps": [g for g in d_gaps if g["priority"] == "CRITICAL"],
                "high_gaps": [g for g in d_gaps if g["priority"] == "HIGH"],
                "all_gaps": d_gaps
            }
        }
    with open(OUTPUT_DIR / "district_analysis.json", "w", encoding="utf-8") as f:
        json.dump(districts_analysis_json, f, indent=2)

    # 3. skill_gaps.json
    skill_gaps_json = {
        "metadata": meta,
        "priority_thresholds": {
            "CRITICAL": ">= 50",
            "HIGH": "30-49",
            "MEDIUM": "15-29",
            "LOW": "< 15"
        },
        "priority_distribution": gap_data["priority_counts"],
        "statewide_summary": gap_data["statewide_gaps"],
        "all_gap_records": gap_data["all_gap_records"],
        "by_district": gap_data["district_gaps"]
    }
    with open(OUTPUT_DIR / "skill_gaps.json", "w", encoding="utf-8") as f:
        json.dump(skill_gaps_json, f, indent=2)

    # 4. course_alignment.json
    course_alignment_json = {
        "metadata": meta,
        "total_courses_evaluated": len(aligned_courses),
        "courses": aligned_courses
    }
    with open(OUTPUT_DIR / "course_alignment.json", "w", encoding="utf-8") as f:
        json.dump(course_alignment_json, f, indent=2)

    # 5. training_plans.json
    training_plans_json = {
        "metadata": meta,
        "state_summary": training_plans["state_summary"],
        "district_plans": training_plans["district_plans"]
    }
    with open(OUTPUT_DIR / "training_plans.json", "w", encoding="utf-8") as f:
        json.dump(training_plans_json, f, indent=2)

    print(f"\n[OK] Pipeline completed successfully!")
    print(f"     Generated 5 output files in {OUTPUT_DIR}:")
    print(f"     1. dashboard.json")
    print(f"     2. district_analysis.json")
    print(f"     3. skill_gaps.json")
    print(f"     4. course_alignment.json")
    print(f"     5. training_plans.json")

    return {
        "status": "SUCCESS",
        "total_jobs": total_jobs,
        "total_courses": len(dfs["courses"]),
        "gaps_count": len(gap_data["all_gap_records"]),
        "priority_counts": gap_data["priority_counts"],
        "output_directory": str(OUTPUT_DIR)
    }


if __name__ == "__main__":
    run_pipeline()

