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



