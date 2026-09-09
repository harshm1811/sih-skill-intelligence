"""
Module: skill_normalization
Purpose: Maintains the taxonomy mapping to normalize skill variations.
"""

# Taxonomy mapping variants to Canonical Names
SKILL_TAXONOMY = {
    # Data & Analytics
    "powerbi": "Power BI",
    "power bi": "Power BI",
    "microsoft power bi": "Power BI",
    "excel": "Excel",
    "ms excel": "Excel",
    "sql": "SQL",
    "mysql": "SQL",
    "postgresql": "SQL",
    
    # Programming & Development
    "python": "Python",
    "python3": "Python",
    "java": "Java",
    "c++": "C++",
    "cpp": "C++",
    "js": "JavaScript",
    "javascript": "JavaScript",
    
    # AI & ML
    "ml": "Machine Learning",
    "machine learning": "Machine Learning",
    "ai": "Artificial Intelligence",
    "artificial intelligence": "Artificial Intelligence",
    "nlp": "Natural Language Processing",
    
    # General Tech / Cloud
    "aws": "AWS",
    "amazon web services": "AWS",
    "azure": "Microsoft Azure",
    "gcp": "Google Cloud Platform"
}

def normalize_skill(raw_term: str) -> str:
    """
    Normalizes a raw skill string to its canonical taxonomy name.
    If not found in the taxonomy, returns the title-cased raw term.
    """
    clean_term = raw_term.strip().lower()
    return SKILL_TAXONOMY.get(clean_term, clean_term.title())