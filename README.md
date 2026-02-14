# Triage-Plus-Plus
Triage++ SOC Automation Project
#  Triage++ – SOC Automation Platform

Triage++ is a Security Operations Center (SOC) Automation Platform designed to intelligently score, classify, and route security alerts using rule-based logic and machine learning.

It reduces analyst fatigue, minimizes false positives, and enables faster incident response.

---

##  Core Capabilities

-  ML-based Risk Scoring Engine
-  Automated Decision Logic (Suppress / Queue / Escalate)
-  Real-time Elastic + Kibana Integration
-  Risk Threshold Visualization Dashboard
-  Dockerized Deployment
-  PostgreSQL Support
-  Elastic Bulk Alert Injection
-  Alert Explainability Layer

---
# Triage-Plus-Plus

##  Architecture Overview

Elastic Alerts
      ↓
Triage++ Engine
      ↓
Risk Scoring + Normalization
      ↓
Decision Layer (Suppress / Queue / Escalate)
      ↓
Elastic Writer
      ↓
Kibana Dashboard


---

##  Decision Logic

| Risk Score | Decision   |
|------------|------------|
| ≤ 35       | SUPPRESS   |
| 36 – 50    | QUEUE      |
| > 50       | ESCALATE   |

---

##  Dashboard Highlights

- Executive KPIs (Escalation Rate / Queue Rate / Suppress Rate)
- Risk Distribution Histogram
- Decision Alignment Chart
- Alert Trend Over Time
- Investigation Queue Table
- Global Risk Health Indicator

---

##  Machine Learning Layer

- Feature normalization
- Customer risk profiling
- Model training via scikit-learn
- Serialized model inference (model.pkl)

---

##  Tech Stack

- Python (FastAPI)
- Elasticsearch
- Kibana
- PostgreSQL
- SQLAlchemy
- scikit-learn
- Docker
- PowerShell (bulk alert simulation)

---

##  Setup

### 1️ Clone the repository

```bash
git clone git@github.com:Ibrahem86/Triage-Plus-Plus.git
cd Triage-Plus-Plus

2️⃣ Create virtual environment
python -m venv venv
venv\Scripts\activate

3️⃣ Install dependencies
pip install -r requirements.txt

Run the application
uvicorn app.main:app --reload

🧪 Alert Simulation

PowerShell bulk script available to generate:

False positive waves

Escalation spikes

Queue overload scenarios

🧩 Future Enhancements

Adaptive thresholding

Behavior-based anomaly scoring

SOAR integration

Multi-tenant support

Cloud-native deployment

