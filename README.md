# Maharashtra Skill Intelligence & Curriculum Alignment Platform — Backend

**Smart India Hackathon 2026** | **Problem Statement 26134**  
*Challenges in aligning skill development programs with industry requirements and emerging job market demands.*

**Role**: Person 2 — Backend Developer  
**Core Pipeline Story**:  
`Industry Demand` ➔ `Skill Gap` ➔ `Course Action` ➔ `District Training Plan`

---

## 1. Installation

### Prerequisites
- Python 3.10+ (tested with Python 3.14)
- `pip`

### Steps
1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```

2. (Optional but recommended) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 2. Running the API

Start the FastAPI application:

```bash
# Option A (Simplest - directly run script):
python main.py

# Option B (Using Uvicorn reload):
uvicorn main:app --reload --port 8000
```

Once running:
- **API Base URL**: `http://localhost:8000`
- **Interactive Swagger Docs**: `http://localhost:8000/docs`
- **Alternative ReDoc UI**: `http://localhost:8000/redoc`

*Note: CORS is enabled for all origins (`"*"`) so Person 1's frontend (e.g. Vite React on `http://localhost:5173` or `http://localhost:3000`) can connect without configuration.*

---

## 3. Available Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/dashboard` | Statewide aggregate metrics (reads `analytics/output/dashboard.json`) |
| `GET` | `/api/districts` | List all districts & stats (reads `analytics/output/district_analysis.json`) |
| `GET` | `/api/districts/{district_id}` | Single district intelligence (jobs, roles, skills, critical gaps) |
| `GET` | `/api/skills/gaps` | **[Data Analytics]** Filterable gaps by `?district=Pune` & `?priority=CRITICAL` (`skill_gaps.json`) |
| `GET` | `/api/skills/{skill_id}/gap?district={district}` | Single skill gap metrics (industry demand vs training coverage) |
| `GET` | `/api/courses/alignment` | **[Data Analytics]** Batch course throughput & alignment scores (`course_alignment.json`) |
| `GET` | `/api/courses/{course_id}` | Single course curriculum alignment & missing syllabus skills |
| `GET` | `/api/recommendations?district={district}&skill={skill}` | Specific course/syllabus actions and lab upgrades |
| `GET` | `/api/districts/training-plans` | **[Data Analytics]** All district training plans (`training_plans.json`) |
| `GET` | `/api/training-plan/{district}` | Single district training plan roadmap & trainee targets |
| `POST` | `/api/analyze-jd` | **[AI Agent]** Analyze job description text via NLP skill extractor (`process_job_description`) |
| `GET` | `/` | Health check and API metadata |

---

## 4. Example API Requests & Responses

### 1. Statewide Dashboard
**Request:**
```http
GET /api/dashboard
```
**Response (200 OK):**
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
**Request:**
```http
GET /api/districts/pune
```
**Response (200 OK):**
```json
{
  "district": "Pune",
  "total_jobs": 3240,
  "top_roles": [
    "Data Analyst",
    "CNC Programmer",
    "AutoCAD Designer",
    "Full Stack Developer",
    "Quality Control Engineer"
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

### 3. Skill Gap Analysis
**Request:**
```http
GET /api/skills/power-bi/gap?district=Pune
```
**Response (200 OK):**
```json
{
  "skill": "Power BI",
  "district": "Pune",
  "industry_demand": 82,
  "training_coverage": 27,
  "gap": 55,
  "priority": "CRITICAL"
}
```

---

### 4. Course Curriculum Alignment
**Request:**
```http
GET /api/courses/CS-102
```
**Response (200 OK):**
```json
{
  "course_id": "CS-102",
  "course_name": "Diploma in Computer Applications & Analytics",
  "institution_type": "Polytechnic / ITI",
  "covered_skills": [
    "Excel",
    "Basic SQL",
    "C Programming"
  ],
  "missing_emerging_skills": [
    "Power BI",
    "Cloud Fundamentals",
    "Python for Data"
  ],
  "alignment_score": 58,
  "status": "NEEDS_REVIEW",
  "last_updated": "2022-06-15"
}
```

---

### 5. Actionable Recommendations
**Request:**
```http
GET /api/recommendations?district=Pune&skill=power-bi
```
**Response (200 OK):**
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
**Request:**
```http
GET /api/training-plan/pune
```
**Response (200 OK):**
```json
{
  "district": "Pune",
  "total_target_trainees": 1850,
  "priority_sectors": [
    "IT & ITES",
    "Automotive & Manufacturing"
  ],
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
    },
    {
      "skill": "Cloud Infrastructure",
      "target_trainees": 400,
      "target_institutes": [
        "ITI Haveli",
        "COEP Technological University Skill Center"
      ],
      "recommended_course_action": "Launch AWS/Azure Cloud Fundamentals certification track",
      "timeline_months": 3
    },
    {
      "skill": "AutoCAD & 3D Modeling",
      "target_trainees": 400,
      "target_institutes": [
        "Government ITI Pune (Girls)",
        "Chakan Auto Cluster Center"
      ],
      "recommended_course_action": "Integrate GD&T and 3D parametric CAD into semester 2",
      "timeline_months": 3
    }
  ]
}
```

---

### 7. AI Job Description Analysis (NLP Skill Extraction)
**Request:**
```http
POST /api/analyze-jd
Content-Type: application/json

{
  "job_description": "Hiring a Data Analyst in Pune with experience in Power BI, SQL, and Python for industrial dashboards."
}
```
**Response (200 OK):**
```json
{
  "status": "success",
  "inferred_role": "Data Analyst",
  "district": "Pune",
  "extracted_skills": [
    "Power Bi",
    "Python",
    "Sql"
  ],
  "confidence_score": 0.88,
  "skills_count": 3,
  "source": "ai_agent"
}
```

---

## 5. Architectural Notes for Team Members

- **Person 1 (Frontend)**: All responses follow the exact agreed JSON structure. No auth headers required.
- **Person 3 (Data/Analytics)**: Place your processed datasets or analytics routines into `app/services/` or `app/data/`. The route handlers call service methods, keeping your data pipelines decoupled from HTTP concerns.
- **Person 4 (AI/NLP Team)**: Generative course recommendations or skill extraction logic should replace or enhance `app/services/recommendation_service.py` and `app/services/skill_service.py`.
