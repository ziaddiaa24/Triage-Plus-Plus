from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.api.schemas import AlertIn
from app.core.engine import engine
from app.core.normalizer import normalize_alert

from app.data.postgres import SessionLocal
from app.data.models import AlertMetrics, TrainingSample

from app.integrations.elastic_writer import index_triage_result

router = APIRouter()

# ======================================================
# Health Check
# ======================================================

@router.get("/ping")
def ping():
    return {"status": "ok", "service": "Triage++ Intake Layer"}

# ======================================================
# Manual / API Alert Intake
# ======================================================

@router.post("/alerts/evaluate")
def evaluate_alert(alert: AlertIn):
    """
    Accept alerts from API / testing / non-Elastic sources
    """
    normalized = normalize_alert(alert.dict())
    decision = engine.evaluate(normalized)

    # 🔥 Write decision to Elasticsearch
    index_triage_result(decision)

    return decision

# ======================================================
# Elastic Intake (Webhook)
# ======================================================

@router.post("/elastic/alerts")
async def ingest_elastic_alert(request: Request):
    """
    Accept alerts directly from Elastic Webhook actions
    """
    payload = await request.json()

    alerts = payload.get("alerts") or [payload]
    results = []

    for raw_alert in alerts:
        normalized = normalize_alert(raw_alert)
        decision = engine.evaluate(normalized)

        # 🔥 Index every decision
        index_triage_result(decision)

        results.append(decision)

    return {
        "received": len(alerts),
        "processed": len(results),
        "results": results
    }

# ======================================================
# Metrics APIs
# ======================================================

@router.get("/metrics")
def metrics():
    db = SessionLocal()
    data = db.query(AlertMetrics).all()
    db.close()

    return {m.key: m.count for m in data}

@router.get("/mlstats")
def ml_stats():
    db = SessionLocal()

    total = db.query(TrainingSample).count()
    escalated = (
        db.query(TrainingSample)
        .filter(TrainingSample.decision == 1)
        .count()
    )
    suppressed = total - escalated

    db.close()

    return {
        "total": total,
        "escalated": escalated,
        "suppressed": suppressed,
        "noise_reduction": round((suppressed / total) * 100, 2) if total else 0
    }

# ======================================================
# Executive Dashboard (Lightweight SOC View)
# ======================================================

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    return """
<!DOCTYPE html>
<html>
<head>
<title>Triage++ SOC Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>

<body style="
    font-family: Arial;
    background: #020617;
    color: #e5e7eb;
    text-align: center;
    padding: 20px;
">

<h1 style="color:#38bdf8;">Triage++ Executive Dashboard</h1>
<p>Noise Reduction & Decision Efficiency</p>

<div id="stats" style="margin:20px;"></div>

<canvas id="chart" width="500" height="250"></canvas>

<script>
Promise.all([
    fetch('/api/v1/mlstats').then(r => r.json())
]).then(([ml]) => {

document.getElementById("stats").innerHTML = `
    <h3>Total Alerts: ${ml.total}</h3>
    <h3 style="color:#ef4444;">Escalated: ${ml.escalated}</h3>
    <h3 style="color:#22c55e;">Suppressed: ${ml.suppressed}</h3>
    <h3 style="color:#38bdf8;">Noise Reduction: ${ml.noise_reduction}%</h3>
`;

new Chart(document.getElementById("chart"), {
    type: 'doughnut',
    data: {
        labels: ['Escalated', 'Suppressed'],
        datasets: [{
            data: [ml.escalated, ml.suppressed],
            backgroundColor: ['#ef4444', '#22c55e']
        }]
    },
    options: {
        plugins: {
            legend: {
                labels: {
                    color: '#e5e7eb'
                }
            }
        }
    }
});
});
</script>

</body>
</html>
"""
