"""
Quick Terminal Preview for Maharashtra Skill Intelligence Platform
Run this to see a formatted summary of your analytical results in the terminal.

Usage:
    python preview.py
"""

import json
from pathlib import Path

OUTPUT_DIR = Path("analytics/output")


def print_dashboard():
    dash_file = OUTPUT_DIR / "dashboard.json"
    plans_file = OUTPUT_DIR / "training_plans.json"
    gaps_file = OUTPUT_DIR / "skill_gaps.json"

    if not dash_file.exists():
        print("[!] Output files not found. Please run 'python run_analytics.py' first.")
        return

    with open(dash_file, "r", encoding="utf-8") as f:
        dash = json.load(f)

    with open(gaps_file, "r", encoding="utf-8") as f:
        gaps = json.load(f)

    with open(plans_file, "r", encoding="utf-8") as f:
        plans = json.load(f)

    kpis = dash["kpis"]

    print("\n" + "=" * 70)
    print("   MAHARASHTRA SKILL INTELLIGENCE PLATFORM (SIH 2026 - PS 26134)")
    print("=" * 70)
    print(f"  * Status:                      PROTOTYPE RUNNING")
    print(f"  * Jobs Analyzed:               {kpis['total_job_postings']:,}")
    print(f"  * Vocational Courses:          {kpis['total_training_courses']}")
    print(f"  * Total Enrolled Seats:        {kpis['total_enrolled_capacity']:,}")
    print(f"  * Annual Completers:           {kpis['total_annual_completers']:,}")
    print(f"  * Annual Placements:           {kpis['total_annual_placements']:,} ({int(kpis['overall_placement_rate']*100)}% Placement Rate)")
    print(f"  * Critical Skill Gaps:         {kpis['critical_skill_gaps']} skills (Gap >= 50)")
    print("=" * 70)

    print("\n[+] DISTRICT SUMMARY:")
    print(f"  {'District':<26} {'Jobs':<8} {'Courses':<10} {'Capacity':<10} {'Critical Gaps'}")
    print("  " + "-" * 66)
    for card in dash["district_summaries"]:
        print(f"  {card['district']:<26} {card['jobs_count']:<8} {card['courses_count']:<10} {card['training_capacity']:<10} {card['critical_gaps']}")

    print("\n[+] TOP 5 STATEWIDE CRITICAL SKILL GAPS:")
    print(f"  {'Skill':<28} {'Category':<24} {'Demand':<8} {'Coverage':<10} {'Gap'}")
    print("  " + "-" * 76)
    for g in gaps["statewide_summary"][:5]:
        print(f"  {g['skill']:<28} {g['category']:<24} {g['statewide_demand']:<8} {g['statewide_coverage']:<10} {g['statewide_gap']}")

    print("\n[+] SAMPLE ACTION PLAN (PUNE):")
    pune_plan = plans["district_plans"]["Pune"]
    print(f"  Current Courses: {pune_plan['current_status']['active_courses_count']} | Current Capacity: {pune_plan['current_status']['total_current_capacity']}")
    print(f"  Target Additional Seats: +{pune_plan['action_plan']['targeted_additional_seats']} seats")
    print("  Proposed New Courses:")
    for nc in pune_plan["action_plan"]["new_courses_to_introduce"]:
        print(f"    - {nc['proposed_course']} (+{nc['proposed_capacity']} seats)")
        print(f"      Target Skills: {', '.join(nc['target_skills'])}")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    print_dashboard()

