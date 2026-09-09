import re
from typing import Dict, List, Any
from skill_normalization import SKILL_TAXONOMY, normalize_skill

# A simple list of recognizable roles for the prototype
KNOWN_ROLES = [
    "Data Analyst", "Data Scientist", "Software Engineer", 
    "Frontend Developer", "Backend Developer", "Machine Learning Engineer"
]

PROFICIENCY_KEYWORDS = {
    "basic": ["basic", "fundamental", "beginner", "familiar with", "exposure to"],
    "intermediate": ["intermediate", "proficient", "working knowledge", "capable"],
    "advanced": ["advanced", "expert", "master", "deep understanding", "highly proficient"]
}

def extract_role(text: str) -> str:
    """Extracts the job role from the text if it matches a known role."""
    for role in KNOWN_ROLES:
        if role.lower() in text.lower():
            return role
    return "Unknown Role"

def determine_proficiency(text: str, skill: str) -> dict:
    """
    Looks for proficiency keywords in the vicinity of the skill.
    Defaults to Intermediate if no clear modifier is found.
    """
    cleaned_text = text.lower()
    skill_lower = skill.lower()
    
    # Look for keywords within a ~30 character window before or after the skill
    window_size = 40
    skill_idx = cleaned_text.find(skill_lower)
    
    if skill_idx != -1:
        start = max(0, skill_idx - window_size)
        end = min(len(cleaned_text), skill_idx + len(skill_lower) + window_size)
        context_window = cleaned_text[start:end]
        
        for level, keywords in PROFICIENCY_KEYWORDS.items():
            for kw in keywords:
                if kw in context_window:
                    return {"level": level.capitalize(), "inferred": False}
                    
    # Default behavior
    return {"level": "Intermediate", "inferred": True}
def extract_all_known_skills(text: str) -> List[str]:
    """
    Finds known skills in the text using word boundaries and returns 
    a list of their normalized canonical names.
    """
    found_skills = set()
    lower_text = text.lower()
    
    # We use regex word boundaries (\b) so we don't accidentally match 
    # 'c' inside 'machine' or 'java' inside 'javascript'.
    for variant in SKILL_TAXONOMY.keys():
        pattern = r'\b' + re.escape(variant) + r'\b'
        if re.search(pattern, lower_text):
            found_skills.add(normalize_skill(variant))
            
    return list(found_skills)
def process_job_description(jd_text: str) -> dict:
    """
    Main pipeline function for JD -> Skill extraction.
    """
    role = extract_role(jd_text)
    extracted_skills = extract_all_known_skills(jd_text)
    
    skills_with_proficiency = []
    for skill in extracted_skills:
        prof = determine_proficiency(jd_text, skill)
        skills_with_proficiency.append({
            "skill": skill,
            "proficiency": prof["level"],
            "inferred": prof["inferred"]
        })
        
    return {
        "role": role,
        "skills": skills_with_proficiency
    }