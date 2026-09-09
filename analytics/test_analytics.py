"""
Comprehensive Verification and Test Suite for Analytics Engine
Validates mathematical consistency, JSON contracts, and schema integrity.
"""

import json
import os
import unittest
from pathlib import Path
import pandas as pd

from analytics.config import (
    DATA_DIR,
    OUTPUT_DIR,
    DISTRICTS,
    GAP_THRESHOLD_CRITICAL,
    GAP_THRESHOLD_HIGH,
    GAP_THRESHOLD_MEDIUM
)


class TestAnalyticsEngine(unittest.TestCase):

    def test_01_csv_files_exist_and_non_empty(self):
        """Verify all 8 source CSV files exist and have data."""
        expected_files = [
            "districts.csv", "skills.csv", "jobs.csv", "job_skills.csv",
            "courses.csv", "course_skills.csv", "employers.csv", "placements.csv"
        ]
        for fname in expected_files:
            fpath = DATA_DIR / fname
            self.assertTrue(fpath.exists(), f"Missing file: {fname}")
            df = pd.read_csv(fpath)
            self.assertGreater(len(df), 0, f"File {fname} is empty")

    def test_02_output_json_files_exist(self):
        """Verify all 5 JSON output files exist in analytics/output/."""
        expected_jsons = [
            "dashboard.json", "district_analysis.json",
            "skill_gaps.json", "course_alignment.json", "training_plans.json"
        ]
        for jname in expected_jsons:
            jpath = OUTPUT_DIR / jname
            self.assertTrue(jpath.exists(), f"Missing output JSON: {jname}")

    def test_03_skill_gap_mathematical_consistency(self):
        """
        STRICT CONSISTENCY TEST:
        Asserts that for 100% of records in skill_gaps.json:
          skill_gap == industry_demand - training_coverage
        and priority corresponds strictly to threshold rules.
        """
        with open(OUTPUT_DIR / "skill_gaps.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        records = data["all_gap_records"]
        self.assertGreater(len(records), 0)

        for rec in records:
            demand = rec["industry_demand"]
            coverage = rec["training_coverage"]
            gap = rec["skill_gap"]
            priority = rec["priority"]

            # Exact math assertion
            self.assertEqual(
                gap,
                demand - coverage,
                f"Math inconsistency in record: {rec}"
            )

            # Priority classification check
            if gap >= GAP_THRESHOLD_CRITICAL:
                expected_priority = "CRITICAL"
            elif gap >= GAP_THRESHOLD_HIGH:
                expected_priority = "HIGH"
            elif gap >= GAP_THRESHOLD_MEDIUM:
                expected_priority = "MEDIUM"
            else:
                expected_priority = "LOW"

            self.assertEqual(
                priority,
                expected_priority,
                f"Priority mismatch for gap={gap} in record: {rec}"
            )

    def test_04_course_effectiveness_math(self):
        """Verify course effectiveness score matches completion_rate * placement_rate."""
        with open(OUTPUT_DIR / "course_alignment.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        courses = data["courses"]
        self.assertEqual(len(courses), 15)

        for c in courses:
            comp_rate = c["completion_rate"]
            place_rate = c["placement_rate"]
            expected_eff = round(comp_rate * place_rate, 4)
            self.assertAlmostEqual(
                c["effectiveness_score"],
                expected_eff,
                places=4,
                msg=f"Effectiveness score mismatch in course {c['course_id']}"
            )

    def test_05_district_coverage(self):
        """Verify all 5 target districts are represented across outputs."""
        with open(OUTPUT_DIR / "district_analysis.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        for d in DISTRICTS:
            self.assertIn(d, data["districts"], f"District {d} missing from district_analysis.json")

        with open(OUTPUT_DIR / "training_plans.json", "r", encoding="utf-8") as f:
            plans = json.load(f)

        for d in DISTRICTS:
            self.assertIn(d, plans["district_plans"], f"District {d} missing from training_plans.json")


if __name__ == "__main__":
    unittest.main(verbosity=2)

