"""Quick test for consolidated backend files (main.py, services.py, data.py)."""
import sys
from pathlib import Path
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

import data
import services
from main import (
    get_dashboard,
    list_districts,
    get_district,
    get_skill_gap,
    get_course,
    get_recommendations,
    get_training_plan,
    analyze_job_description,
    get_all_skill_gaps,
    get_courses_alignment,
    get_all_training_plans,
    JobDescriptionRequest,
    DashboardMetrics,
    DistrictDetail,
    SkillGapResponse,
    CourseDetail,
    RecommendationResponse,
    DistrictTrainingPlanResponse,
)

def run():
    print("Testing consolidated backend...")
    data.init_db()

    d = DashboardMetrics(**get_dashboard())
    assert d.total_jobs == 12450
    print(f"1. Dashboard: OK ({d.total_jobs} jobs, {d.critical_gaps} gaps)")

    districts = list_districts()
    assert len(districts) == 5
    print(f"2. Districts: OK ({[x['name'] for x in districts]})")

    pune = DistrictDetail(**get_district("pune"))
    assert pune.district == "Pune"
    print(f"3. District Detail: OK ({pune.district}, {len(pune.top_skills)} skills)")

    gap = SkillGapResponse(**get_skill_gap("power-bi", "Pune"))
    assert gap.gap == 55
    print(f"4. Skill Gap: OK ({gap.skill}: Demand {gap.industry_demand} vs Coverage {gap.training_coverage})")

    c = CourseDetail(**get_course("CS-102"))
    assert c.alignment_score == 58
    print(f"5. Course Alignment: OK ({c.course_id} score: {c.alignment_score})")

    rec = RecommendationResponse(**get_recommendations("Pune", "power-bi"))
    assert len(rec.actions) >= 3
    print(f"6. Recommendations: OK ({rec.priority} priority, {len(rec.actions)} actions)")

    tp = DistrictTrainingPlanResponse(**get_training_plan("pune"))
    assert tp.total_target_trainees == 1850
    print(f"7. Training Plan: OK ({tp.district}, {tp.total_target_trainees} trainees)")

    jd_res = analyze_job_description(JobDescriptionRequest(text="Need Python and Power BI analyst in Pune"))
    assert "Power Bi" in jd_res["extracted_skills"]
    print(f"8. AI Skill Extraction (POST /api/analyze-jd): OK ({jd_res['extracted_skills']})")

    # Person 3 Data Analytics Contracts
    all_gaps = get_all_skill_gaps(district="Pune", priority="CRITICAL")
    assert len(all_gaps) >= 1
    print(f"9. Batch Skill Gaps (GET /api/skills/gaps?district=Pune&priority=CRITICAL): OK ({len(all_gaps)} critical gaps)")

    course_align = get_courses_alignment()
    assert len(course_align) >= 1
    print(f"10. Course Alignment (GET /api/courses/alignment): OK ({len(course_align)} courses)")

    training_plans = get_all_training_plans()
    assert len(training_plans) >= 1
    print(f"11. Batch Training Plans (GET /api/districts/training-plans): OK ({len(training_plans)} district plans)")

    print("\n==================================================")
    print("ALL CONSOLIDATED BACKEND TESTS PASSED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    run()

