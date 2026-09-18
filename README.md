# Maharashtra Skill Intelligence & Curriculum Alignment Platform

**Smart India Hackathon 2026** | **Problem Statement 26134**  
*Challenges in aligning skill development programs with industry requirements and emerging job market demands.*

**Core Pipeline Story**:  
`Industry Demand (Job Postings & Skills)` ➔ `Skill Gap (Deficit Index & Priorities)` ➔ `Course Action (Syllabus Revisions)` ➔ `District Training Plan (Actionable Allocations)`

---

## 1. Project Directory Structure

Every file in this repository has a dedicated role in the end-to-end intelligence pipeline:

```
sih-skill-intelligence/
├── main.py                     # [Backend] FastAPI server, Pydantic data contracts, and all 11 REST endpoints
├── services.py                 # [Backend] Intelligence layer connecting Analytics, AI/NLP, and API routes
├── data.py                     # [Backend] SQLite database initialization, fallback data, and JSON loader
├── skill_intelligence.db       # [Database] SQLite local database
│
├── skill_extraction.py         # [AI / NLP] Extracts roles, normalized skills, and proficiency from raw JD text
├── skill_normalization.py      # [AI / NLP] Skill taxonomy dictionary mapping variants to canonical names
├── recommendation_engine.py    # [AI / Logic] Business rule engine generating targeted course & lab interventions
│
├── run_analytics.py            # [Analytics] Main script to execute the complete data processing pipeline
├── preview.py                  # [Analytics] Terminal CLI report showing statewide KPIs, districts & top gaps
│
├── analytics/                  # [Analytics Engine]
│   ├── config.py               # Weights, thresholds, and scoring parameters
│   ├── loader.py               # Ingestion and validation for CSV datasets
│   ├── demand_engine.py        # Industry demand scoring from job market postings
│   ├── supply_engine.py        # Vocational/educational training supply scoring
│   ├── gap_engine.py           # Quantitative skill gap computation and priority rating
│   ├── alignment_engine.py     # Curriculum alignment scoring & missing skill detection
│   ├── district_planner.py     # District-level seat expansion & lab modernization planner
│   ├── test_analytics.py       # Unit tests for analytics pipeline engines
│   └── output/                 # Pre-calculated JSON outputs served by the API:
│       ├── dashboard.json          # Statewide summary metrics and top roles
│       ├── district_analysis.json  # Per-district statistics, top skills, and employers
│       ├── skill_gaps.json         # Quantified skill gap metrics with priority levels
│       ├── course_alignment.json   # Course alignment scores and missing syllabus skills
│       └── training_plans.json     # Actionable district training proposals and seat allocations
│
├── data/                       # [Raw Datasets] Representative Maharashtra industry & education data (CSVs):
│   ├── jobs.csv                # Active job postings with district, company, and experience
│   ├── job_skills.csv          # Extracted technical skills mapped to job postings
│   ├── courses.csv             # Vocational and technical training courses catalog
│   ├── course_skills.csv       # Skills currently covered in existing syllabi
│   ├── districts.csv           # Maharashtra district profiles and economic sectors
│   ├── employers.csv           # Major employers and hiring industries
│   ├── skills.csv              # Standardized skill taxonomy definitions
│   └── placements.csv          # Institutional placement history records
│
├── test_backend.py             # [Testing] Automated test suite verifying all 11 API endpoints and contracts
├── test_analytics.py           # [Testing] Unit tests for NLP extraction, normalization, and recommendations
├── requirements.txt            # Python dependencies (FastAPI, Uvicorn, Pandas, Pydantic)
├── vercel.json                 # [Deployment] Root Vercel deployment config for Vite frontend
├── .gitignore                  # Git ignore rules for virtual environments, caches, and local DBs
├── README.md                   # Complete system documentation
│
└── frontend/                   # [Frontend] React 18 + Vite Web Application
    ├── package.json            # Node.js dependencies and build scripts
    ├── vite.config.js          # Vite build configuration
    ├── vercel.json             # SPA routing rewrite rules for Vercel
    ├── index.html              # HTML entry point
    └── src/                    # React source code (components, pages, services, styles)
```

---

## 2. Installation & Quickstart

### Prerequisites
- Python 3.10+ (tested on Python 3.14) & `pip`
- Node.js 18+ & `npm` (for the React frontend)

### Step 1: Clone and Navigate
```bash
git clone https://github.com/your-repo/sih-skill-intelligence.git
cd sih-skill-intelligence
```

### Step 2: Set up Backend Dependencies
```bash
# (Optional) Create virtual environment
python -m venv venv
# Windows: venv\Scripts\activate | macOS/Linux: source venv/bin/activate

# Install Python requirements
pip install -r requirements.txt
```

### Step 3: Set up Frontend Dependencies
```bash
cd frontend
npm install
cd ..
```

---

## 3. How to Run

### A. Run Data Analytics Pipeline
Process raw CSVs in `data/` through analytical engines and generate verified JSONs in `analytics/output/`:
```bash
python run_analytics.py
```

### B. View Terminal Summary Preview
Display a clean, formatted terminal summary of KPIs, district tables, and sample action plans:
```bash
python preview.py
```

### C. Start FastAPI Backend Server
Run the REST API server on `http://localhost:8000`:
```bash
# Option 1 (Direct script execution):
python main.py

# Option 2 (Uvicorn with live reload):
uvicorn main:app --reload --port 8000
```
* **API Base URL**: `http://localhost:8000`
* **Interactive Swagger UI**: `http://localhost:8000/docs`
* **Alternative ReDoc UI**: `http://localhost:8000/redoc`
* **CORS**: Enabled for all origins (`"*"`) for seamless frontend connection (Vite/React).

### D. Start React Frontend (Vite Dev Server)
In a separate terminal, launch the client-side UI:
```bash
cd frontend
npm run dev
```
* **Frontend Local URL**: `http://localhost:5173`

### E. Run Automated Test Suites
```bash
# Run backend API contract tests (11/11 tests pass):
python test_backend.py

# Run NLP extraction, normalization, and recommendation tests:
python test_analytics.py
```

### F. Cloud Deployment (Vercel)
The repository includes `vercel.json` configured for zero-config Vercel deployment:
- **Build Command**: `cd frontend && npm install && npm run build`
- **Output Directory**: `frontend/dist`
- **Framework**: `vite`
- SPA client-side routes automatically route to `/index.html`.

---

## 4. API Endpoints Reference

All endpoints return clean JSON conforming to agreed team contracts:

| Method | Endpoint | Source File | Description |
|---|---|---|---|
| `GET` | `/api/dashboard` | `analytics/output/dashboard.json` | Statewide aggregate metrics (jobs, skills, critical gaps, courses needing review) |
| `GET` | `/api/districts` | `analytics/output/district_analysis.json` | List all monitored Maharashtra districts with summary stats |
| `GET` | `/api/districts/{district_id}` | `analytics/output/district_analysis.json` | Single district intelligence (active jobs, top roles, top skills, critical gaps) |
| `GET` | `/api/skills/gaps` | `analytics/output/skill_gaps.json` | Filterable skill gaps by `?district=Pune` and/or `?priority=CRITICAL` |
| `GET` | `/api/skills/{skill_id}/gap?district={district}` | `services.py` | Single skill gap metrics (industry demand vs training coverage) |
| `GET` | `/api/courses/alignment` | `analytics/output/course_alignment.json` | Batch course throughput, alignment scores, and missing syllabus skills |
| `GET` | `/api/courses` | `services.py` | Catalog of monitored vocational & technical courses |
| `GET` | `/api/courses/{course_id}` | `services.py` | Single course syllabus details and curriculum review status |
| `GET` | `/api/recommendations?district={district}&skill={skill}` | `recommendation_engine.py` | Specific curriculum actions, new modules, and lab upgrades |
| `GET` | `/api/districts/training-plans` | `analytics/output/training_plans.json` | Complete training plans across all Maharashtra districts |
| `GET` | `/api/training-plan/{district}` | `analytics/output/training_plans.json` | Single district training roadmap, trainee targets, and partner ITIs |
| `POST` | `/api/analyze-jd` | `skill_extraction.py` | AI/NLP skill extraction from raw job description strings |
| `GET` | `/` | `main.py` | Health check and API information |

---

## 5. Example API Requests & Responses

### 1. Statewide Dashboard
```http
GET /api/dashboard
```
```json
{
  "total_jobs": 12450,
  "total_skills": 48,
  "critical_gaps": 17,
  "courses_needing_review": 12
}
```

---

### 2. District Overview
```http
GET /api/districts/pune
```
```json
{
  "district": "Pune",
  "total_jobs": 3240,
  "top_roles": [
    "Data Analyst",
    "CNC Programmer",
    "AutoCAD Designer",
    "Full Stack Developer"
  ],
  "top_skills": [
    "Power BI",
    "Python",
    "CNC Milling",
    "AutoCAD",
    "PLC Programming"
  ],
  "critical_gaps": [
    "Power BI",
    "CNC Milling",
    "Cloud Infrastructure"
  ]
}
```

---

### 3. Filterable Skill Gaps (Data Analytics)
```http
GET /api/skills/gaps?district=Pune&priority=CRITICAL
```
```json
[
  {
    "skill": "Power BI",
    "district": "Pune",
    "industry_demand": 82,
    "training_coverage": 27,
    "gap": 55,
    "priority": "CRITICAL"
  },
  {
    "skill": "CNC Milling",
    "district": "Pune",
    "industry_demand": 88,
    "training_coverage": 35,
    "gap": 53,
    "priority": "CRITICAL"
  }
]
```

---

### 4. Course Curriculum Alignment
```http
GET /api/courses/CS-102
```
```json
{
  "course_id": "CS-102",
  "course_name": "Diploma in Computer Applications & Analytics",
  "institution_type": "Polytechnic / ITI",
  "covered_skills": ["Excel", "Basic SQL", "C Programming"],
  "missing_emerging_skills": ["Power BI", "Cloud Fundamentals", "Python for Data"],
  "alignment_score": 58,
  "status": "NEEDS_REVIEW",
  "last_updated": "2022-06-15"
}
```

---

### 5. Actionable Recommendations
```http
GET /api/recommendations?district=Pune&skill=power-bi
```
```json
{
  "priority": "HIGH",
  "skill": "Power BI",
  "district": "Pune",
  "actions": [
    "Add intermediate Power BI",
    "Add practical dashboard project",
    "Increase lab hours"
  ]
}
```

---

### 6. District Training Plan
```http
GET /api/training-plan/pune
```
```json
{
  "district": "Pune",
  "total_target_trainees": 1850,
  "priority_sectors": ["IT & ITES", "Automotive & Manufacturing"],
  "skill_initiatives": [
    {
      "skill": "Power BI",
      "target_trainees": 450,
      "target_institutes": [
        "Government ITI Aundh",
        "Government Polytechnic Pune"
      ],
      "recommended_course_action": "Introduce 40-hour hands-on BI & Data Visualization module",
      "timeline_months": 3
    },
    {
      "skill": "CNC Milling",
      "target_trainees": 600,
      "target_institutes": [
        "Bhosari Industry Skill Cluster",
        "ITI Pimpri"
      ],
      "recommended_course_action": "Upgrade CNC simulator lab to modern multi-axis setup",
      "timeline_months": 4
    }
  ]
}
```

---

### 7. AI Job Description Skill Extraction
```http
POST /api/analyze-jd
Content-Type: application/json

{
  "job_description": "Looking for a Data Analyst proficient in Python, SQL, Power BI, and basic AWS in Pune."
}
```
```json
{
  "role": "Data Analyst",
  "skills": [
    {
      "skill": "Python",
      "proficiency": "Intermediate",
      "inferred": false
    },
    {
      "skill": "SQL",
      "proficiency": "Intermediate",
      "inferred": true
    },
    {
      "skill": "Power BI",
      "proficiency": "Intermediate",
      "inferred": true
    },
    {
      "skill": "AWS",
      "proficiency": "Basic",
      "inferred": false
    }
  ]
}
```

---

## 6. Team Ownership & Responsibilities

| Role | Member | Primary Modules & Files |
|---|---|---|
| **Person 1** | Frontend Developer | `frontend/` (React 18 + Vite SPA, pages, components, `vercel.json`) |
| **Person 2** | Backend Developer | `main.py`, `services.py`, `data.py`, `test_backend.py`, CORS setup |
| **Person 3** | Data & Analytics | `data/*.csv`, `analytics/`, `run_analytics.py`, `preview.py` |
| **Person 4** | AI / NLP Engineer | `skill_extraction.py`, `skill_normalization.py`, `recommendation_engine.py` |
| **Person 5** | Integration & QA | `test_backend.py`, `test_analytics.py`, API contract validation & documentation |
