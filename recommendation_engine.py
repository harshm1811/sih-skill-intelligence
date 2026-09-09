from typing import Dict, Any, List

"""
Module: recommendation_engine
Purpose: Generates actionable training plans based on quantitative skill gaps.
"""

def generate_recommendation(
    district: str, 
    skill: str, 
    industry_demand: int, 
    training_coverage: int, 
    skill_gap: float, 
    course_coverage: float
) -> Dict[str, Any]:
    """
    Applies transparent business rules to generate curriculum alignment recommendations.
    """
    
    recommendation = {
        "district": district,
        "skill": skill,
        "demand_metrics": {
            "industry_demand": industry_demand,
            "training_coverage": training_coverage,
            "skill_gap": skill_gap,
            "course_coverage": course_coverage
        },
        "priority": "UNKNOWN",
        "actions": [],
        "reason": ""
    }
    
    if skill_gap >= 50:
        recommendation["priority"] = "CRITICAL"
        recommendation["actions"] = [
            f"Add advanced/intermediate {skill} modules",
            "Increase practical training",
            "Add industry project",
            "Review trainer capability"
        ]
        recommendation["reason"] = f"Industry demand significantly exceeds current training coverage (Gap: {skill_gap}%)."
        
    elif 30 <= skill_gap < 50:
        recommendation["priority"] = "MODERATE"
        recommendation["actions"] = [
            f"Strengthen existing {skill} module",
            "Add practical component",
            "Validate employer requirements"
        ]
        recommendation["reason"] = f"Moderate gap identified (Gap: {skill_gap}%). Current curriculum requires reinforcement."
        
    else:
        recommendation["priority"] = "LOW"
        recommendation["actions"] = [
            "Monitor demand",
            "Maintain current curriculum"
        ]
        recommendation["reason"] = f"Supply aligns well with demand (Gap: {skill_gap}%). No immediate intervention required."
        
    return recommendation

def _optional_llm_insights(recommendation_data: Dict[str, Any]) -> str:
    """
    OPTIONAL: Stub for future LLM integration. 
    Not required for core Hackathon prototype functionality.
    """
    # Example: response = external_api_call(prompt=f"Analyze this gap: {recommendation_data}")
    return "LLM integration pending - currently operating via transparent rule engine."