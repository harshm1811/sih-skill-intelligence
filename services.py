"""
services.py - Business Logic & Intelligence Layer.
Encapsulates:
- Skill Gap Analysis (Industry Demand vs Institutional Coverage)
- Course Curriculum Alignment
- Recommendation Generation
- District Training Plan Roadmap
- AI/NLP Job Description Processing (Person 4 hook)
"""

import re
from typing import Dict, Any, List, Optional
from fastapi import HTTPException

from data import (
    DASHBOARD_DATA,
    DISTRICTS_DATA,
    SKILLS_GAP_DATA,
    COURSES_DATA,
    RECOMMENDATIONS_DATA,
    TRAINING_PLANS_DATA,
    load_analytics_json,
)

# -------------------------------------------------------------
# 1. AI & NLP Job Description Skill Extractor (Person 4 Hook)
# -------------------------------------------------------------
_external_nlp_fn = None

# Attempt dynamic import if Person 4 provides a standalone file
for mod_name in ["ai", "nlp", "extractor", "process_jd"]:
    try:
        mod = __import__(mod_name, fromlist=["process_job_description"])
        if hasattr(mod, "process_job_description"):
            _external_nlp_fn = getattr(mod, "process_job_description")
            break
    except ImportError:
        pass


def process_job_description(text: str) -> Dict[str, Any]:
    """
    Skill extraction logic for Job Descriptions.
    Extracts in-demand technical skills, inferred job role, and location context.
    """
    if _external_nlp_fn is not None:
        try:
            res = _external_nlp_fn(text)
            if isinstance(res, dict):
                return res
            return {"status": "success", "result": res}
        except Exception as e:
            pass  # Fall through to built-in extractor

    text_lower = text.lower()
    known_skills = [
        "power bi", "python", "sql", "excel", "tableau", "aws", "azure",
        "cloud", "cnc milling", "cnc programming", "autocad", "plc programming",
        "scada", "cybersecurity", "react", "fastapi", "machine learning",
        "ev powertrain", "solar pv", "metrology", "hplc", "gmp"
    ]
    detected_skills = [
        s.title() for s in known_skills if re.search(rf"\b{re.escape(s)}\b", text_lower)
    ]

    districts = ["pune", "mumbai", "nagpur", "nashik", "aurangabad", "chhatrapati sambhaji nagar"]
    detected_district = "Pune"
    for d in districts:
        if d in text_lower:
            detected_district = d.title()
            break

    role_candidates = [
        "data analyst", "full stack developer", "cloud engineer", "cnc programmer",
        "autocad designer", "quality engineer", "technician", "electrician"
    ]
    detected_role = "Technical Specialist"
    for r in role_candidates:
        if r in text_lower:
            detected_role = r.title()
            break

    return {
        "status": "success",
        "inferred_role": detected_role,
        "district": detected_district,
        "extracted_skills": detected_skills if detected_skills else ["General Technical Skills"],
        "confidence_score": 0.88,
        "skills_count": len(detected_skills),
        "source": "ai_agent" if _external_nlp_fn else "builtin_nlp_extractor",
    }


# -------------------------------------------------------------
# 2. Statewide Dashboard Service
# -------------------------------------------------------------
def get_dashboard_metrics() -> Dict[str, Any]:
    analytics_data = load_analytics_json("dashboard.json")
    if analytics_data:
        return analytics_data
    return {
        "total_jobs": DASHBOARD_DATA["total_jobs"],
        "total_skills": DASHBOARD_DATA["total_skills"],
        "critical_gaps": DASHBOARD_DATA["critical_gaps"],
        "courses_needing_review": DASHBOARD_DATA["courses_needing_review"],
    }


# -------------------------------------------------------------
# 3. Districts Intelligence Service
# -------------------------------------------------------------
def _normalize_district_id(district_id: str) -> str:
    norm = district_id.strip().lower().replace(" ", "").replace("-", "")
    aliases = {
        "pune": "pune",
        "mumbai": "mumbai",
        "nagpur": "nagpur",
        "nashik": "nashik",
        "aurangabad": "sambhajinagar",
        "sambhajinagar": "sambhajinagar",
        "chhatrapatisambhajinagar": "sambhajinagar",
    }
    return aliases.get(norm, norm)


def get_all_districts() -> Any:
    analytics_districts = load_analytics_json("district_analysis.json")
    if analytics_districts:
        return analytics_districts
    return [
        {
            "id": d["id"],
            "name": d["name"],
            "total_jobs": d["total_jobs"],
            "critical_gaps_count": len(d["critical_gaps"]),
            "top_sector": d["top_sector"],
        }
        for d in DISTRICTS_DATA.values()
    ]


def get_district_detail(district_id: str) -> Dict[str, Any]:
    norm_id = _normalize_district_id(district_id)
    dist = DISTRICTS_DATA.get(norm_id)
    if not dist:
        for d in DISTRICTS_DATA.values():
            if d["name"].lower() == district_id.strip().lower():
                dist = d
                break

    if not dist:
        available = ", ".join([d["name"] for d in DISTRICTS_DATA.values()])
        raise HTTPException(status_code=404, detail=f"District '{district_id}' not found. Available: {available}")

    return {
        "district": dist["name"],
        "total_jobs": dist["total_jobs"],
        "top_roles": dist["top_roles"],
        "top_skills": dist["top_skills"],
        "critical_gaps": dist["critical_gaps"],
    }


# -------------------------------------------------------------
# 4. Skill Gap Analytics Service
# -------------------------------------------------------------
def get_skill_gap(skill_id: str, district: str) -> Dict[str, Any]:
    def norm(s: str):
        return s.strip().lower().replace(" ", "-").replace("_", "")

    norm_skill = norm(skill_id)
    norm_dist = norm(district)

    for (s_key, d_key), val in SKILLS_GAP_DATA.items():
        if (s_key == norm_skill or norm(val["skill"]) == norm_skill) and (
            d_key == norm_dist or norm(val["district"]) == norm_dist
        ):
            return val

    # Baseline estimate for dynamically requested skills
    return {
        "skill": skill_id.replace("-", " ").title(),
        "district": district.title(),
        "industry_demand": 72,
        "training_coverage": 35,
        "gap": 37,
        "priority": "HIGH",
    }


# -------------------------------------------------------------
# 5. Course Alignment Service
# -------------------------------------------------------------
def get_course_detail(course_id: str) -> Dict[str, Any]:
    course = COURSES_DATA.get(course_id.strip().upper())
    if not course:
        for k, v in COURSES_DATA.items():
            if k.lower() == course_id.strip().lower():
                course = v
                break

    if not course:
        available = ", ".join(COURSES_DATA.keys())
        raise HTTPException(status_code=404, detail=f"Course '{course_id}' not found. Available: {available}")

    return course


def get_all_courses() -> List[Dict[str, Any]]:
    return list(COURSES_DATA.values())


# -------------------------------------------------------------
# 6. Recommendation Engine Service
# -------------------------------------------------------------
def get_recommendations(district: Optional[str], skill: str) -> Dict[str, Any]:
    def norm(s: str):
        return s.strip().lower().replace(" ", "-").replace("_", "")

    norm_skill = norm(skill)
    norm_dist = norm(district) if district else ""

    for (d_key, s_key), data in RECOMMENDATIONS_DATA.items():
        if s_key == norm_skill and (not norm_dist or d_key == norm_dist):
            return data

    formatted = skill.replace("-", " ").title()
    return {
        "priority": "HIGH",
        "skill": formatted,
        "district": district.title() if district else None,
        "actions": [
            f"Add hands-on lab modules for practical {formatted} application",
            f"Introduce industry-guided capstone project focusing on {formatted}",
            f"Organize faculty development workshop on modern {formatted} industry workflows",
            f"Embed {formatted} assessment milestones in semester evaluation",
        ],
    }


# -------------------------------------------------------------
# 7. District Training Plan Roadmap Service
# -------------------------------------------------------------
def get_district_training_plan(district: str) -> Dict[str, Any]:
    norm_key = _normalize_district_id(district)
    plan = TRAINING_PLANS_DATA.get(norm_key)

    if not plan:
        for p in TRAINING_PLANS_DATA.values():
            if p["district"].lower() == district.strip().lower():
                plan = p
                break

    if not plan:
        raise HTTPException(
            status_code=404,
            detail=f"Training plan for district '{district}' not found.",
        )

    return plan


# -------------------------------------------------------------
# 8. Batch Analytics Services (Person 3 Data/Analytics Contracts)
# -------------------------------------------------------------
def get_all_skill_gaps(
    district: Optional[str] = None, priority: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Reads analytics/output/skill_gaps.json if present (fallback to representative dataset).
    Supports filtering by ?district=Pune and ?priority=CRITICAL.
    """
    items = load_analytics_json("skill_gaps.json")
    if not items:
        items = list(SKILLS_GAP_DATA.values())

    if district:
        d_lower = district.strip().lower()
        items = [i for i in items if i.get("district", "").strip().lower() == d_lower]

    if priority:
        p_upper = priority.strip().upper()
        items = [i for i in items if i.get("priority", "").strip().upper() == p_upper]

    return items


def get_courses_alignment() -> Any:
    """Reads analytics/output/course_alignment.json if present (fallback to representative dataset)."""
    data_json = load_analytics_json("course_alignment.json")
    if data_json:
        return data_json
    return list(COURSES_DATA.values())


def get_all_training_plans() -> Any:
    """Reads analytics/output/training_plans.json if present (fallback to representative dataset)."""
    data_json = load_analytics_json("training_plans.json")
    if data_json:
        return data_json
    return list(TRAINING_PLANS_DATA.values())

