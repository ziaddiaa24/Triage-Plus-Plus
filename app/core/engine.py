from app.analyzers.repetition import repetition_score
from app.analyzers.behavior import behavior_score
from app.analyzers.threat_intel import vt_ip_score
from app.metrics.collector import increment
from app.integrations.elastic_writer import index_triage_result

import joblib


# =============================
# Load ML model (optional / internal)
# =============================
try:
    model = joblib.load("model.pkl")
except Exception as e:
    print(f"[WARN] ML model not loaded: {e}")
    model = None


class TriageEngine:

    def evaluate(self, alert: dict):
        # -----------------------------
        # Metrics
        # -----------------------------
        increment("total_alerts")

        # -----------------------------
        # Intelligence Layers
        # -----------------------------
        rep_ctx = repetition_score(alert)  # dict: level / count / description

        beh_score, beh_msg, beh_impact = behavior_score(alert)

        intel_score, intel_msg, intel_impact = vt_ip_score(
            alert.get("source_ip"),
            category=alert.get("category", "generic"),
            customer_id=alert.get("customer_id")
        )

        # Safety: force numeric
        beh_score = int(beh_score or 0)
        intel_score = int(intel_score or 0)

        # -----------------------------
        # Base Score
        # -----------------------------
        base = {
            "HIGH": 50,
            "MEDIUM": 35,
            "LOW": 20
        }.get(alert.get("severity", "MEDIUM"), 35)

        # -----------------------------
        # Final Numeric Risk
        # (repetition is contextual, not numeric)
        # -----------------------------
        final_score = base + beh_score + intel_score

        # -----------------------------
        # Primary Decision Logic
        # -----------------------------
        if final_score >= 80:
            decision = "ESCALATE"
            confidence = "HIGH"
            decision_reason = "High cumulative risk score"

        elif final_score >= 60:
            decision = "ESCALATE"
            confidence = "MEDIUM"
            decision_reason = "Moderate risk score"

        elif final_score >= 35:
            decision = "QUEUE"
            confidence = "LOW"
            decision_reason = "Suspicious but below escalation threshold"

        else:
            decision = "SUPPRESS"
            confidence = "LOW"
            decision_reason = "Low risk activity"

        # -----------------------------
        # Repetition as Contextual Modifier
        # -----------------------------
        if rep_ctx.get("level") == "high" and decision != "ESCALATE":
            decision = "ESCALATE"
            confidence = "MEDIUM"
            decision_reason = "Persistent repeated activity detected"

        # -----------------------------
        # Build Result Object
        # -----------------------------
        result = {
            "alert_id": alert.get("alert_id"),
            "decision": decision,
            "confidence": confidence,
            "decision_reason": decision_reason,

            "scores": {
                "base": base,
                "behavior": beh_score,
                "threat_intel": intel_score,
                "final_score": final_score
            },

            "context": {
                "repetition": rep_ctx,
                "asset": alert.get("asset"),
                "user": alert.get("user"),
                "source_ip": alert.get("source_ip")
            },

            "explainability": {
                "behavior": {
                    "impact": beh_impact,
                    "details": beh_msg
                },
                "threat_intel": {
                    "impact": intel_impact,
                    "details": intel_msg
                }
            }
        }

        # -----------------------------
        # Index result into Elasticsearch
        # -----------------------------
        try:
            index_triage_result(result)
        except Exception as e:
            print(f"[WARN] Failed to index triage result: {e}")

        return result


engine = TriageEngine()
