import hashlib
from datetime import datetime
from app.data.postgres import SessionLocal
from app.data.models import RepetitionPattern


def _fingerprint(alert: dict) -> str:
    """
    Generate a stable fingerprint for repetition tracking
    """
    rule = alert.get("rule_name", "unknown_rule")
    src_ip = alert.get("source_ip", "unknown_ip")
    asset = alert.get("asset", "unknown_asset")

    raw = f"{rule}|{src_ip}|{asset}"
    return hashlib.sha256(raw.encode()).hexdigest()


def get_repetition_count(alert: dict) -> int:
    """
    Track repetition count in DB and return current count
    """
    fp = _fingerprint(alert)
    now = datetime.utcnow()

    db = SessionLocal()
    record = db.get(RepetitionPattern, fp)

    if not record:
        record = RepetitionPattern(
            fingerprint=fp,
            count=1,
            first_seen=now,
            last_seen=now
        )
        db.add(record)
        db.commit()
        db.close()
        return 1

    record.count += 1
    record.last_seen = now
    count = record.count

    db.commit()
    db.close()
    return count


def repetition_score(alert: dict) -> dict:
    """
    Contextual repetition analysis (NO direct scoring)
    Used only as a modifier with threat intelligence
    """
    count = get_repetition_count(alert)

    if count >= 20:
        return {
            "level": "high",
            "count": count,
            "description": f"Repeated {count} times (strong persistence)"
        }

    elif count >= 10:
        return {
            "level": "medium",
            "count": count,
            "description": f"Repeated {count} times (moderate repetition)"
        }

    else:
        return {
            "level": "low",
            "count": count,
            "description": f"Repeated {count} times (low repetition)"
        }
