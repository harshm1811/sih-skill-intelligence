import json
import sqlite3
from pathlib import Path
from typing import Dict, Any, List, Optional

DB_PATH = Path(__file__).resolve().parent / "skill_intelligence.db"


def load_analytics_json(filename: str) -> Optional[Any]:
    """
    Attempts to load pre-calculated JSON output from Person 3 (Data & Analytics).
    Searches in ../analytics/output/ and ./analytics/output/.
    Returns parsed JSON if found, else None.
    """
    possible_paths = [
        Path(__file__).resolve().parent.parent / "analytics" / "output" / filename,
        Path(__file__).resolve().parent / "analytics" / "output" / filename,
        Path.cwd() / "analytics" / "output" / filename,
        Path.cwd().parent / "analytics" / "output" / filename,
    ]
    for p in possible_paths:
        if p.exists():
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
    return None

DASHBOARD_DATA = {
    "total_jobs": 12450,
    "total_skills": 48,
    "critical_gaps": 17,
    "courses_needing_review": 12,
}

DISTRICTS_DATA = {
    "pune": {
        "id": "pune",
        "name": "Pune",
        "district": "Pune",
        "total_jobs": 3240,
        "top_roles": [
            "Data Analyst",
            "CNC Programmer",
            "AutoCAD Designer",
            "Full Stack Developer",
            "Quality Control Engineer",
        ],
        "top_skills": [
            "Power BI",
            "Python",
            "CNC Milling",
            "AutoCAD",
            "PLC Programming",
        ],
        "critical_gaps": [
            "Power BI",
            "CNC Milling",
            "Cloud Infrastructure",
        ],
        "top_sector": "Automotive & IT Hub",
        "priority_sectors": ["IT & ITES", "Automotive & Manufacturing"],
    },
    "mumbai": {
        "id": "mumbai",
        "name": "Mumbai",
        "district": "Mumbai",
        "total_jobs": 4890,
        "top_roles": [
            "Financial Analyst",
            "Cloud Solutions Architect",
            "Cybersecurity Analyst",
            "Full Stack Developer",
            "Digital Marketer",
        ],
        "top_skills": [
            "Cloud Infrastructure",
            "Power BI",
            "Python",
            "Cybersecurity",
            "Financial Modeling",
        ],
        "critical_gaps": [
            "Cybersecurity",
            "Cloud Infrastructure",
            "Generative AI Fundamentals",
        ],
        "top_sector": "BFSI & Tech Services",
        "priority_sectors": ["BFSI & FinTech", "IT & Cloud Services"],
    },
    "nagpur": {
        "id": "nagpur",
        "name": "Nagpur",
        "district": "Nagpur",
        "total_jobs": 1620,
        "top_roles": [
            "Supply Chain Coordinator",
            "EV Powertrain Technician",
            "Industrial Electrician",
            "Solar PV Installer",
            "GIS Analyst",
        ],
        "top_skills": [
            "EV Powertrain Diagnostics",
            "Warehouse Management Systems",
            "Solar PV Maintenance",
            "PLC Programming",
            "AutoCAD",
        ],
        "critical_gaps": [
            "EV Powertrain Diagnostics",
            "Solar PV Maintenance",
            "Warehouse Management Systems",
        ],
        "top_sector": "Logistics & Green Energy",
        "priority_sectors": ["Logistics & Warehousing", "Renewable Energy & EV"],
    },
    "nashik": {
        "id": "nashik",
        "name": "Nashik",
        "district": "Nashik",
        "total_jobs": 1420,
        "top_roles": [
            "Tool & Die Maker",
            "Precision Machining Tech",
            "Industrial IoT Technician",
            "Agri-Tech Field Specialist",
            "Mechatronics Operator",
        ],
        "top_skills": [
            "CNC Milling",
            "Industrial IoT Sensors",
            "Precision Metrology",
            "AutoCAD",
            "Pneumatics",
        ],
        "critical_gaps": [
            "Industrial IoT Sensors",
            "CNC Milling",
            "Precision Metrology",
        ],
        "top_sector": "Precision Auto Components",
        "priority_sectors": ["Auto Components & Engineering", "Agro-Processing & Tech"],
    },
    "sambhajinagar": {
        "id": "sambhajinagar",
        "name": "Chhatrapati Sambhaji Nagar",
        "district": "Chhatrapati Sambhaji Nagar",
        "total_jobs": 1280,
        "top_roles": [
            "Pharma Quality Analyst",
            "HVAC Technician",
            "Industrial Automation Specialist",
            "Machine Maintenance Operator",
        ],
        "top_skills": [
            "HPLC & Chromatography",
            "PLC Programming",
            "SCADA",
            "GMP Compliance",
            "AutoCAD",
        ],
        "critical_gaps": [
            "HPLC & Chromatography",
            "SCADA",
            "Industrial Automation",
        ],
        "top_sector": "Pharma & Heavy Engineering",
        "priority_sectors": ["Pharmaceuticals & Chemicals", "Heavy Engineering & Auto"],
    },
}

SKILLS_GAP_DATA = {
    ("power-bi", "pune"): {
        "skill": "Power BI",
        "district": "Pune",
        "industry_demand": 82,
        "training_coverage": 27,
        "gap": 55,
        "priority": "CRITICAL",
    },
    ("cnc-milling", "pune"): {
        "skill": "CNC Milling",
        "district": "Pune",
        "industry_demand": 88,
        "training_coverage": 35,
        "gap": 53,
        "priority": "CRITICAL",
    },
    ("cloud-infrastructure", "pune"): {
        "skill": "Cloud Infrastructure",
        "district": "Pune",
        "industry_demand": 78,
        "training_coverage": 26,
        "gap": 52,
        "priority": "CRITICAL",
    },
    ("python", "pune"): {
        "skill": "Python",
        "district": "Pune",
        "industry_demand": 75,
        "training_coverage": 50,
        "gap": 25,
        "priority": "MODERATE",
    },
    ("cybersecurity", "mumbai"): {
        "skill": "Cybersecurity",
        "district": "Mumbai",
        "industry_demand": 91,
        "training_coverage": 32,
        "gap": 59,
        "priority": "CRITICAL",
    },
    ("cloud-infrastructure", "mumbai"): {
        "skill": "Cloud Infrastructure",
        "district": "Mumbai",
        "industry_demand": 89,
        "training_coverage": 38,
        "gap": 51,
        "priority": "CRITICAL",
    },
    ("ev-powertrain-diagnostics", "nagpur"): {
        "skill": "EV Powertrain Diagnostics",
        "district": "Nagpur",
        "industry_demand": 84,
        "training_coverage": 22,
        "gap": 62,
        "priority": "CRITICAL",
    },
    ("solar-pv-maintenance", "nagpur"): {
        "skill": "Solar PV Maintenance",
        "district": "Nagpur",
        "industry_demand": 76,
        "training_coverage": 30,
        "gap": 46,
        "priority": "HIGH",
    },
    ("industrial-iot-sensors", "nashik"): {
        "skill": "Industrial IoT Sensors",
        "district": "Nashik",
        "industry_demand": 80,
        "training_coverage": 24,
        "gap": 56,
        "priority": "CRITICAL",
    },
    ("hplc-chromatography", "sambhajinagar"): {
        "skill": "HPLC & Chromatography",
        "district": "Chhatrapati Sambhaji Nagar",
        "industry_demand": 85,
        "training_coverage": 31,
        "gap": 54,
        "priority": "CRITICAL",
    },
}

COURSES_DATA = {
    "CS-102": {
        "course_id": "CS-102",
        "course_name": "Diploma in Computer Applications & Analytics",
        "institution_type": "Polytechnic / ITI",
        "covered_skills": ["Excel", "Basic SQL", "C Programming"],
        "missing_emerging_skills": ["Power BI", "Cloud Fundamentals", "Python for Data"],
        "alignment_score": 58,
        "status": "NEEDS_REVIEW",
        "last_updated": "2022-06-15",
    },
    "ME-201": {
        "course_id": "ME-201",
        "course_name": "Certificate in CNC Machining & CAD/CAM",
        "institution_type": "ITI / Vocational Training Center",
        "covered_skills": ["2D Drafting", "Manual Lathe Operation", "Basic G-Code"],
        "missing_emerging_skills": ["5-Axis CNC Milling", "CAM Simulation", "Precision Metrology"],
        "alignment_score": 52,
        "status": "NEEDS_REVIEW",
        "last_updated": "2021-08-20",
    },
    "EE-301": {
        "course_id": "EE-301",
        "course_name": "Diploma in Industrial Automation & Electrical Systems",
        "institution_type": "Polytechnic",
        "covered_skills": ["Relay Logic", "Basic Motor Drives", "Single Phase Wiring"],
        "missing_emerging_skills": ["PLC Programming", "SCADA Integration", "Industrial IoT Sensors"],
        "alignment_score": 64,
        "status": "NEEDS_REVIEW",
        "last_updated": "2022-03-10",
    },
    "EV-401": {
        "course_id": "EV-401",
        "course_name": "Advanced Certificate in Electric Vehicle Maintenance",
        "institution_type": "Vocational Skill Institute",
        "covered_skills": ["Battery Cell Testing", "BMS Basics", "High Voltage Safety"],
        "missing_emerging_skills": ["CAN Bus Diagnostics", "Regenerative Braking Systems"],
        "alignment_score": 82,
        "status": "ALIGNED",
        "last_updated": "2025-01-15",
    },
    "IT-501": {
        "course_id": "IT-501",
        "course_name": "Cloud Computing & DevOps Foundations",
        "institution_type": "Polytechnic / Autonomous Institute",
        "covered_skills": ["Linux Admin", "Docker Basics", "AWS Core Services"],
        "missing_emerging_skills": ["Kubernetes", "Infrastructure as Code (Terraform)"],
        "alignment_score": 86,
        "status": "ALIGNED",
        "last_updated": "2025-05-12",
    },
}

RECOMMENDATIONS_DATA = {
    ("pune", "power-bi"): {
        "priority": "HIGH",
        "skill": "Power BI",
        "district": "Pune",
        "actions": [
            "Add intermediate Power BI",
            "Add practical dashboard project",
            "Increase lab hours",
        ],
    },
    ("pune", "cnc-milling"): {
        "priority": "HIGH",
        "skill": "CNC Milling",
        "district": "Pune",
        "actions": [
            "Partner with Bhosari industrial cluster for multi-axis CNC access",
            "Include mastercam simulation before physical machining",
            "Schedule mandatory 3-week shop-floor internship",
        ],
    },
    ("pune", "cloud-infrastructure"): {
        "priority": "HIGH",
        "skill": "Cloud Infrastructure",
        "district": "Pune",
        "actions": [
            "Introduce AWS/Azure cloud practitioner certification voucher program",
            "Set up virtualized cloud sandbox for polytechnic students",
            "Update CS curriculum from on-prem sysadmin to cloud-native ops",
        ],
    },
    ("mumbai", "cybersecurity"): {
        "priority": "HIGH",
        "skill": "Cybersecurity",
        "district": "Mumbai",
        "actions": [
            "Set up hands-on cyber defense & SOC analyst simulation lab",
            "Integrate CERT-In compliance guidelines into curriculum",
            "Add real-world vulnerability assessment capstone project",
        ],
    },
    ("nagpur", "ev-powertrain-diagnostics"): {
        "priority": "HIGH",
        "skill": "EV Powertrain Diagnostics",
        "district": "Nagpur",
        "actions": [
            "Procure dedicated EV cut-section powertrain training bench",
            "Conduct 'Train the Trainer' program with local EV OEMs",
            "Establish safety protocol certifications for high-voltage battery handling",
        ],
    },
}

TRAINING_PLANS_DATA = {
    "pune": {
        "district": "Pune",
        "total_target_trainees": 1850,
        "priority_sectors": ["IT & ITES", "Automotive & Manufacturing"],
        "skill_initiatives": [
            {
                "skill": "Power BI",
                "target_trainees": 450,
                "target_institutes": [
                    "Government ITI Aundh",
                    "Government Polytechnic Pune",
                ],
                "recommended_course_action": "Introduce 40-hour hands-on BI & Data Visualization module",
                "timeline_months": 3,
            },
            {
                "skill": "CNC Milling",
                "target_trainees": 600,
                "target_institutes": [
                    "Bhosari Industry Skill Cluster",
                    "ITI Pimpri",
                ],
                "recommended_course_action": "Upgrade CNC simulator lab to modern multi-axis setup",
                "timeline_months": 4,
            },
            {
                "skill": "Cloud Infrastructure",
                "target_trainees": 400,
                "target_institutes": [
                    "ITI Haveli",
                    "COEP Technological University Skill Center",
                ],
                "recommended_course_action": "Launch AWS/Azure Cloud Fundamentals certification track",
                "timeline_months": 3,
            },
            {
                "skill": "AutoCAD & 3D Modeling",
                "target_trainees": 400,
                "target_institutes": [
                    "Government ITI Pune (Girls)",
                    "Chakan Auto Cluster Center",
                ],
                "recommended_course_action": "Integrate GD&T and 3D parametric CAD into semester 2",
                "timeline_months": 3,
            },
        ],
    },
    "mumbai": {
        "district": "Mumbai",
        "total_target_trainees": 2200,
        "priority_sectors": ["BFSI & FinTech", "IT & Cloud Services"],
        "skill_initiatives": [
            {
                "skill": "Cybersecurity & SOC Operations",
                "target_trainees": 700,
                "target_institutes": [
                    "Government Polytechnic Mumbai (Bandra)",
                    "Veermata Jijabai Technological Institute (VJTI) Skill Cell",
                ],
                "recommended_course_action": "Deploy virtual cyber range for defensive SOC monitoring",
                "timeline_months": 4,
            },
            {
                "skill": "Cloud Infrastructure",
                "target_trainees": 850,
                "target_institutes": [
                    "Government ITI Mumbai",
                    "K.J. Somaiya Vocational Training Institute",
                ],
                "recommended_course_action": "Establish hybrid cloud administration hands-on curriculum",
                "timeline_months": 3,
            },
            {
                "skill": "Financial Modeling & Analytics",
                "target_trainees": 650,
                "target_institutes": [
                    "Sydenham Institute of Skill Development",
                    "Government Polytechnic Thane",
                ],
                "recommended_course_action": "Integrate Python for quantitative finance into commerce diplomas",
                "timeline_months": 3,
            },
        ],
    },
    "nagpur": {
        "district": "Nagpur",
        "total_target_trainees": 1350,
        "priority_sectors": ["Logistics & Warehousing", "Renewable Energy & EV"],
        "skill_initiatives": [
            {
                "skill": "EV Powertrain Diagnostics",
                "target_trainees": 450,
                "target_institutes": [
                    "Government ITI Nagpur",
                    "MIHAN Skill Development Center",
                ],
                "recommended_course_action": "Set up dual-motor EV repair simulator and battery diagnosis lab",
                "timeline_months": 4,
            },
            {
                "skill": "Warehouse Management Systems (WMS)",
                "target_trainees": 500,
                "target_institutes": [
                    "Nagpur Cargo & Logistics Training Hub",
                    "Government Polytechnic Nagpur",
                ],
                "recommended_course_action": "Add RF scanning and automated inventory tracking practicum",
                "timeline_months": 3,
            },
            {
                "skill": "Solar PV Maintenance",
                "target_trainees": 400,
                "target_institutes": [
                    "MEDA Solar Training Center",
                    "Government ITI Hingna",
                ],
                "recommended_course_action": "Deploy rooftop grid-tied inverter maintenance training module",
                "timeline_months": 2,
            },
        ],
    },
    "nashik": {
        "district": "Nashik",
        "total_target_trainees": 1100,
        "priority_sectors": ["Auto Components & Engineering", "Agro-Processing & Tech"],
        "skill_initiatives": [
            {
                "skill": "Industrial IoT Sensors",
                "target_trainees": 400,
                "target_institutes": [
                    "Government ITI Satpur",
                    "Amrutvahini Institute of Polytechnic",
                ],
                "recommended_course_action": "Implement PLC-to-cloud telemetry and sensor interfacing course",
                "timeline_months": 3,
            },
            {
                "skill": "CNC Milling & Metrology",
                "target_trainees": 450,
                "target_institutes": [
                    "Nashik Engineering Cluster (NEC)",
                    "Government ITI Nashik",
                ],
                "recommended_course_action": "Provide certified CMM (Coordinate Measuring Machine) training",
                "timeline_months": 3,
            },
            {
                "skill": "Smart Cold Chain & Agri-Sensors",
                "target_trainees": 250,
                "target_institutes": [
                    "Dindori Agri-Skill Center",
                    "Government ITI Niphad",
                ],
                "recommended_course_action": "Integrate temperature-logger and controlled atmosphere storage ops",
                "timeline_months": 2,
            },
        ],
    },
    "sambhajinagar": {
        "district": "Chhatrapati Sambhaji Nagar",
        "total_target_trainees": 980,
        "priority_sectors": ["Pharmaceuticals & Chemicals", "Heavy Engineering & Auto"],
        "skill_initiatives": [
            {
                "skill": "HPLC & Chromatography",
                "target_trainees": 380,
                "target_institutes": [
                    "Government Polytechnic Aurangabad",
                    "Waluj Industrial Pharma Skill Center",
                ],
                "recommended_course_action": "Establish cleanroom testing simulation and HPLC instrument calibration",
                "timeline_months": 4,
            },
            {
                "skill": "SCADA & Industrial Automation",
                "target_trainees": 350,
                "target_institutes": [
                    "Government ITI Aurangabad",
                    "Shendra DMIC Automation Training Center",
                ],
                "recommended_course_action": "Upgrade automation benches with Siemens/Rockwell PLC simulation",
                "timeline_months": 3,
            },
            {
                "skill": "GMP Compliance & Cleanroom Ops",
                "target_trainees": 250,
                "target_institutes": [
                    "Government ITI Paithan",
                    "Chikalthana Training Hub",
                ],
                "recommended_course_action": "Offer certified WHO-GMP hygiene and documentation practices module",
                "timeline_months": 2,
            },
        ],
    },
}


def init_db():
    """Create tables if they do not exist and seed representative data in SQLite."""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dashboard_metrics (
            id INTEGER PRIMARY KEY,
            total_jobs INTEGER,
            total_skills INTEGER,
            critical_gaps INTEGER,
            courses_needing_review INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS districts (
            id TEXT PRIMARY KEY,
            name TEXT,
            total_jobs INTEGER,
            top_sector TEXT
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM dashboard_metrics")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO dashboard_metrics (id, total_jobs, total_skills, critical_gaps, courses_needing_review)
            VALUES (1, ?, ?, ?, ?)
        """, (
            DASHBOARD_DATA["total_jobs"],
            DASHBOARD_DATA["total_skills"],
            DASHBOARD_DATA["critical_gaps"],
            DASHBOARD_DATA["courses_needing_review"]
        ))

    cursor.execute("SELECT COUNT(*) FROM districts")
    if cursor.fetchone()[0] == 0:
        for dist in DISTRICTS_DATA.values():
            cursor.execute("""
                INSERT INTO districts (id, name, total_jobs, top_sector)
                VALUES (?, ?, ?, ?)
            """, (dist["id"], dist["name"], dist["total_jobs"], dist["top_sector"]))

    conn.commit()
    conn.close()

