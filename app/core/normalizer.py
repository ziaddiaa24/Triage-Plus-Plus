from datetime import datetime
import uuid

def normalize_alert(alert: dict) -> dict:
    """
    Convert partial / messy alerts into canonical format
    """

    return {
        "alert_id": alert.get("alert_id") or f"AUTO-{uuid.uuid4()}",
        "rule_name": alert.get("rule_name") or "unknown_rule",

        "severity": (alert.get("severity") or "MEDIUM").upper(),

        "source_ip": alert.get("source_ip") or "0.0.0.0",
        "destination": alert.get("destination") or "unknown",

        "user": alert.get("user") or "unknown",
        "asset": alert.get("asset") or "unknown",

        "timestamp": alert.get("timestamp") or datetime.utcnow()
    }
