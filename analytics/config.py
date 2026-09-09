"""
Configuration and Constants for Analytics Engine
SIH 2026 Problem Statement 26134
"""

import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
ANALYTICS_DIR = BASE_DIR / "analytics"
OUTPUT_DIR = ANALYTICS_DIR / "output"

# Problem Statement & Prototype Metadata
PROBLEM_STATEMENT_ID = "26134"
PROJECT_NAME = "Maharashtra Skill Intelligence & Curriculum Alignment Platform"
PROTOTYPE_VERSION = "1.0.0"
DATASET_DISCLAIMER = (
    "Representative / sample data prepared for SIH 2026 Problem Statement 26134 internal prototype. "
    "Not official government statistics."
)

# Target Districts
DISTRICTS = [
    "Pune",
    "Mumbai",
    "Nagpur",
    "Nashik",
    "Chhatrapati Sambhajinagar"
]

# Skill Gap Priority Thresholds
# Primary Formula: Skill Gap = Industry Demand - Training Coverage
GAP_THRESHOLD_CRITICAL = 50
GAP_THRESHOLD_HIGH = 30
GAP_THRESHOLD_MEDIUM = 15

PRIORITY_CRITICAL = "CRITICAL"
PRIORITY_HIGH = "HIGH"
PRIORITY_MEDIUM = "MEDIUM"
PRIORITY_LOW = "LOW"


def classify_priority(gap: float) -> str:
    """
    Classify skill gap priority according to agreed SIH formula:
      Gap >= 50  -> CRITICAL
      Gap 30-49  -> HIGH
      Gap 15-29  -> MEDIUM
      Gap < 15   -> LOW
    """
    if gap >= GAP_THRESHOLD_CRITICAL:
        return PRIORITY_CRITICAL
    elif gap >= GAP_THRESHOLD_HIGH:
        return PRIORITY_HIGH
    elif gap >= GAP_THRESHOLD_MEDIUM:
        return PRIORITY_MEDIUM
    else:
        return PRIORITY_LOW

