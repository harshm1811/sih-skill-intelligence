"""
District Training Planner
Generates actionable, data-driven District Training Plans to bridge identified skill gaps.
Completes the core SIH narrative:
  Demand Intelligence -> Skill Gap -> Course Action -> District Training Plan
"""

from typing import Dict, Any, List
from .config import DISTRICTS


# District-specific strategic domain mapping for new course proposals
NEW_COURSE_BLUEPRINTS = {
    "Pune": [
        {
            "proposed_course": "Advanced EV Powertrain & Battery Systems",
            "target_skills": ["Battery Management Systems", "Electric Powertrain", "Predictive Maintenance"],
            "target_roles": ["EV Battery Technician", "Robotics Maintenance Tech"],
            "proposed_capacity": 120,
            "justification": "Pune automotive belt (Chakan/Bhosari) has severe deficit in EV mobility technicians."
        },
        {
            "proposed_course": "Full Stack Cloud & DevOps Engineering",
            "target_skills": ["AWS", "Docker", "Kubernetes", "React", "Python"],
            "target_roles": ["Full Stack Developer", "Cloud Architect"],
            "proposed_capacity": 150,
            "justification": "Hinjawadi IT corridor has high software demand with zero existing public vocational coverage."
        }
    ],
    "Mumbai": [
        {
            "proposed_course": "Cloud Data Analytics & AI Workflows",
            "target_skills": ["Power BI", "SQL", "Machine Learning", "Python"],
            "target_roles": ["Data Analyst", "Full Stack Developer"],
            "proposed_capacity": 90,
            "justification": "Financial capital demands enterprise BI reporting and fintech analytical capabilities."
        }
    ],
    "Nagpur": [
        {
            "proposed_course": "Smart Warehouse & Supply Chain Automation",
            "target_skills": ["SAP EWM", "Inventory Management", "Logistics Analytics", "IoT Sensors"],
            "target_roles": ["Warehouse Manager", "Supply Chain Coordinator"],
            "proposed_capacity": 100,
            "justification": "Central India Multi-Modal International Hub Airport and Logistics Park (MIHAN) scaling."
        }
    ],
    "Nashik": [
        {
            "proposed_course": "Renewable Microgrid & Solar Engineering",
            "target_skills": ["Solar PV Design", "Grid Integration", "PLC Programming"],
            "target_roles": ["Solar Grid Engineer", "PLC Programmer"],
            "proposed_capacity": 80,
            "justification": "Growing renewable cluster and agricultural solar pumps in North Maharashtra."
        }
    ],
    "Chhatrapati Sambhajinagar": [
        {
            "proposed_course": "Industrial Robotics & Mechatronics",
            "target_skills": ["Robotics Troubleshooting", "PLC Programming", "SCADA", "Predictive Maintenance"],
            "target_roles": ["PLC Programmer", "Robotics Maintenance Tech"],
            "proposed_capacity": 100,
            "justification": "Support Shendra-Bidkin Industrial City (AURIC) advanced manufacturing plants."
        }
    ]
}


def generate_district_training_plans(
    districts_df: Any,
    gap_data: Dict[str, Any],
    courses_df: Any,
    alignment_data: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Synthesizes gaps, existing course effectiveness, and strategic blueprints
    into localized, actionable District Training Plans.
    """
    district_gaps = gap_data["district_gaps"]
    plans = {}

    for district in DISTRICTS:
        # Filter gaps for this district
        gaps_list = district_gaps.get(district, [])
        critical_gaps = [g for g in gaps_list if g["priority"] == "CRITICAL"]
        high_gaps = [g for g in gaps_list if g["priority"] == "HIGH"]
        medium_gaps = [g for g in gaps_list if g["priority"] == "MEDIUM"]

        # Filter active courses in this district
        dist_courses = [c for c in alignment_data if c["district"] == district]
        current_capacity = sum(c["capacity"] for c in dist_courses)
        current_completers = sum(c["completed_trainees"] for c in dist_courses)
        current_placements = sum(c["placed_trainees"] for c in dist_courses)

        # 1. Action: Course Capacity Expansion (for high performing courses)
        expansion_proposals = []
        for c in dist_courses:
            if c["effectiveness_score"] >= 0.55:
                # Calculate recommended expansion based on deficit of skills it teaches
                proposed_boost = min(60, max(25, int(c["capacity"] * 0.35)))
                expansion_proposals.append({
                    "course_id": c["course_id"],
                    "course_name": c["course_name"],
                    "current_capacity": c["capacity"],
                    "proposed_capacity_increase": proposed_boost,
                    "target_skills_supported": [s["skill"] for s in c["skills_taught"]],
                    "effectiveness_score": c["effectiveness_score"]
                })

        # 2. Action: Curriculum Modernization (inject missing critical skills)
        curriculum_updates = []
        for c in dist_courses:
            if c["missing_critical_skills"]:
                curriculum_updates.append({
                    "course_id": c["course_id"],
                    "course_name": c["course_name"],
                    "recommended_modules_to_add": c["missing_critical_skills"],
                    "objective": "Align syllabus with local employer requirements."
                })

        # 3. Action: New Course Introductions
        new_courses = NEW_COURSE_BLUEPRINTS.get(district, [])

        # Total additional seat capacity targeted
        expansion_seats = sum(e["proposed_capacity_increase"] for e in expansion_proposals)
        new_course_seats = sum(nc["proposed_capacity"] for nc in new_courses)
        total_target_additional_seats = expansion_seats + new_course_seats

        plans[district] = {
            "district": district,
            "current_status": {
                "active_courses_count": len(dist_courses),
                "total_current_capacity": current_capacity,
                "annual_completers": current_completers,
                "annual_placements": current_placements,
                "critical_gaps_count": len(critical_gaps),
                "high_gaps_count": len(high_gaps)
            },
            "top_priority_gaps": [
                {
                    "skill": g["skill"],
                    "category": g["category"],
                    "demand": g["industry_demand"],
                    "coverage": g["training_coverage"],
                    "gap": g["skill_gap"],
                    "priority": g["priority"]
                }
                for g in (critical_gaps + high_gaps)[:8]
            ],
            "action_plan": {
                "course_expansions": expansion_proposals,
                "curriculum_modernizations": curriculum_updates,
                "new_courses_to_introduce": new_courses,
                "targeted_additional_seats": total_target_additional_seats
            }
        }

    return {
        "state_summary": {
            "total_districts": len(DISTRICTS),
            "total_state_additional_seats_needed": sum(
                p["action_plan"]["targeted_additional_seats"] for p in plans.values()
            )
        },
        "district_plans": plans
    }

