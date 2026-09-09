"""
Maharashtra Skill Intelligence & Curriculum Alignment Platform
FastAPI Backend - SIH 2026 Problem Statement 26134

Pipeline Story:
INDUSTRY DEMAND ➔ SKILL GAP ➔ COURSE ACTION ➔ DISTRICT TRAINING PLAN
"""

from contextlib import asynccontextmanager
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, Query, Path, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

import data
import services


# =============================================================
# 1. Pydantic Data Contract Schemas
# =============================================================
class JobDescriptionRequest(BaseModel):
    job_description: Optional[str] = Field(None, description="Raw job description text")
    text: Optional[str] = Field(None, description="Alternative field for job description text")

    @property
    def raw_text(self) -> str:
        return (self.job_description or self.text or "").strip()


class DashboardMetrics(BaseModel):
    total_jobs: int
    total_skills: int
    critical_gaps: int
    courses_needing_review: int


class DistrictSummary(BaseModel):
    id: str
    name: str
    total_jobs: int
    critical_gaps_count: int
    top_sector: str


class DistrictDetail(BaseModel):
    district: str
    total_jobs: int
    top_roles: List[str]
    top_skills: List[str]
    critical_gaps: List[str]


class SkillGapResponse(BaseModel):
    skill: str
    district: str
    industry_demand: int
    training_coverage: int
    gap: int
    priority: str


class CourseDetail(BaseModel):
    course_id: str
    course_name: str
    institution_type: str
    covered_skills: List[str]
    missing_emerging_skills: List[str]
    alignment_score: int
    status: str
    last_updated: str


class RecommendationResponse(BaseModel):
    priority: str
    skill: str
    district: Optional[str] = None
    actions: List[str]


class SkillInitiative(BaseModel):
    skill: str
    target_trainees: int
    target_institutes: List[str]
    recommended_course_action: str
    timeline_months: int


class DistrictTrainingPlanResponse(BaseModel):
    district: str
    total_target_trainees: int
    priority_sectors: List[str]
    skill_initiatives: List[SkillInitiative]


# =============================================================
# 2. Application Setup & CORS Middleware
# =============================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize SQLite database tables and seed data
    data.init_db()
    yield


app = FastAPI(
    title="Maharashtra Skill Intelligence & Curriculum Alignment Platform",
    description="SIH 2026 Problem Statement 26134 - Skill Gap & Curriculum Analytics API",
    version="1.0.0",
    lifespan=lifespan,
)

# Enable CORS for React Frontend (Person 1)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================
# 3. API Endpoints
# =============================================================
@app.get("/api/dashboard", response_model=DashboardMetrics, tags=["Dashboard"])
def get_dashboard():
    """Statewide metrics: total jobs analyzed, skills tracked, critical gaps, courses needing review."""
    return services.get_dashboard_metrics()


@app.get("/api/districts", response_model=List[DistrictSummary], tags=["Districts"])
def list_districts():
    """List all monitored Maharashtra districts."""
    return services.get_all_districts()


@app.get("/api/districts/{district_id}", response_model=DistrictDetail, tags=["Districts"])
def get_district(district_id: str = Path(..., description="District name or slug (e.g. 'pune')")):
    """District intelligence: active jobs, top in-demand roles, skills, and critical gaps."""
    return services.get_district_detail(district_id)


@app.get("/api/skills/{skill_id}/gap", response_model=SkillGapResponse, tags=["Skill Gap"])
def get_skill_gap(
    skill_id: str = Path(..., description="Skill name/slug (e.g. 'power-bi')"),
    district: str = Query(..., description="District name (e.g. 'Pune')"),
):
    """Calculate single skill gap: industry demand vs institutional curriculum coverage."""
    return services.get_skill_gap(skill_id=skill_id, district=district)


@app.get("/api/skills/gaps", tags=["Skill Gap", "Data Analytics"])
def get_all_skill_gaps(
    district: Optional[str] = Query(None, description="Filter by district (e.g. 'Pune')"),
    priority: Optional[str] = Query(None, description="Filter by priority (e.g. 'CRITICAL', 'HIGH')"),
):
    """
    Person 3 Data Analytics endpoint:
    Reads pre-calculated skill gaps from analytics/output/skill_gaps.json with optional filters.
    """
    return services.get_all_skill_gaps(district=district, priority=priority)


@app.get("/api/courses", response_model=List[CourseDetail], tags=["Courses"])
def list_courses():
    """Catalog of tracked vocational and technical education courses."""
    return services.get_all_courses()


@app.get("/api/courses/alignment", tags=["Courses", "Data Analytics"])
def get_courses_alignment():
    """
    Person 3 Data Analytics endpoint:
    Reads pre-calculated course alignment scores & missing skills from analytics/output/course_alignment.json.
    """
    return services.get_courses_alignment()


@app.get("/api/courses/{course_id}", response_model=CourseDetail, tags=["Courses"])
def get_course(course_id: str = Path(..., description="Course code (e.g. 'CS-102')")):
    """Analyze course syllabus alignment and identify missing industry skills."""
    return services.get_course_detail(course_id)


@app.get("/api/recommendations", response_model=RecommendationResponse, tags=["Recommendations"])
def get_recommendations(
    skill: str = Query(..., description="Target skill"),
    district: Optional[str] = Query(None, description="Optional target district"),
):
    """Actionable recommendations: curriculum revisions, new modules, and lab upgrades."""
    return services.get_recommendations(district=district, skill=skill)


@app.get("/api/districts/training-plans", tags=["Training Plan", "Data Analytics"])
def get_all_training_plans():
    """
    Person 3 Data Analytics endpoint:
    Reads pre-calculated training plans across all districts from analytics/output/training_plans.json.
    """
    return services.get_all_training_plans()


@app.get("/api/training-plan/{district}", response_model=DistrictTrainingPlanResponse, tags=["Training Plan"])
def get_training_plan(district: str = Path(..., description="District name (e.g. 'Pune')")):
    """Complete District Training Plan: trainee targets, designated ITIs/colleges, and timelines."""
    return services.get_district_training_plan(district)


@app.post("/api/analyze-jd", response_model=Dict[str, Any], tags=["AI Skill Extraction"])
def analyze_job_description(payload: JobDescriptionRequest = Body(...)):
    """
    AI/NLP Skill Extractor (Person 4 Hook).
    Extracts in-demand technical skills, inferred role, and district from raw job descriptions.
    """
    return services.process_job_description(payload.raw_text)


@app.get("/", tags=["Health"])
def root():
    return {
        "status": "healthy",
        "service": "Maharashtra Skill Intelligence API",
        "hackathon": "Smart India Hackathon 2026",
        "problem_statement": "26134",
        "docs_url": "/docs",
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

