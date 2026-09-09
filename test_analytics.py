import unittest
from skill_normalization import normalize_skill
from skill_extraction import process_job_description
from recommendation_engine import generate_recommendation

class TestAnalyticsModule(unittest.TestCase):

    def test_skill_normalization(self):
        self.assertEqual(normalize_skill("power bi"), "Power BI")
        self.assertEqual(normalize_skill("ML"), "Machine Learning")
        self.assertEqual(normalize_skill("UnknownSkill"), "Unknownskill") # Fallback to title case

    def test_skill_extraction(self):
        # We added "Also needs basic AWS" to test a different proficiency level explicitly
        jd_text = "We are looking for a Data Analyst proficient in Python, SQL, Power BI and Excel. Also needs basic AWS."
        
        # Use the updated function name
        result = process_job_description(jd_text)
        
        self.assertEqual(result["role"], "Data Analyst")
        
        # Verify skills were extracted
        extracted_skill_names = [s["skill"] for s in result["skills"]]
        self.assertIn("Python", extracted_skill_names)
        self.assertIn("Excel", extracted_skill_names)
        self.assertIn("AWS", extracted_skill_names)
        
        # Verify proficiency detection based on your 40-character window
        for skill_data in result["skills"]:
            if skill_data["skill"] == "Python":
                # 'proficient' maps to Intermediate in your dictionary
                self.assertEqual(skill_data["proficiency"], "Intermediate")
                self.assertFalse(skill_data["inferred"])
                
            elif skill_data["skill"] == "AWS":
                # 'basic' maps to Basic in your dictionary
                self.assertEqual(skill_data["proficiency"], "Basic")
                self.assertFalse(skill_data["inferred"])

    def test_recommendation_engine_critical(self):
        rec = generate_recommendation(
            district="Pune",
            skill="Power BI",
            industry_demand=500,
            training_coverage=100,
            skill_gap=80.0,  # >= 50
            course_coverage=20.0
        )
        self.assertEqual(rec["priority"], "CRITICAL")
        self.assertIn("Review trainer capability", rec["actions"])

    def test_recommendation_engine_low(self):
        rec = generate_recommendation(
            district="Mumbai",
            skill="Python",
            industry_demand=500,
            training_coverage=450,
            skill_gap=10.0,  # < 30
            course_coverage=90.0
        )
        self.assertEqual(rec["priority"], "LOW")
        self.assertIn("Monitor demand", rec["actions"])

if __name__ == '__main__':
    unittest.main()