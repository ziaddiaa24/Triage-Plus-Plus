from datetime import datetime

def normalize_elastic_alert(alert: dict) -> dict:
    return {
        "alert_id": alert.get("_id") or alert.get("id"),
        "rule_name": alert.get("rule", {}).get("name", "Unknown Rule"),
        "severity": alert.get("severity", "MEDIUM").upper(),
        "source_ip": (
            alert.get("source", {}).get("ip")
            or alert.get("host", {}).get("ip")
            or "0.0.0.0"
        ),
        "destination": alert.get("destination", {}).get("domain", "unknown"),
        "user": alert.get("user", {}).get("name"),
        "asset": alert.get("host", {}).get("name", "unknown"),
        "timestamp": alert.get("@timestamp") or datetime.utcnow().isoformat()
    }
