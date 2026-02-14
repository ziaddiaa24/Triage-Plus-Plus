from datetime import datetime
from app.data.postgres import SessionLocal
from app.data.models import BehaviorBaseline


def behavior_score(alert):
    """
    Behavior analysis:
    - Detect new or rare user/IP behavior per asset
    - Returns: score, message, impact
    """

    user = alert.get("user", "unknown")
    asset = alert.get("asset", "unknown")
    source_ip = alert.get("source_ip", "unknown")

    user_key = f"{user}@{asset}"
    ip_key = f"{source_ip}@{asset}"

    db = SessionLocal()
    now = datetime.utcnow()

    score = 0
    messages = []
    impact = "neutral"

    for key, label in [
        (user_key, "user"),
        (ip_key, "ip")
    ]:
        record = db.get(BehaviorBaseline, key)

        if not record:
            # New behavior
            record = BehaviorBaseline(
                key=key,
                count=1,
                first_seen=now,
                last_seen=now
            )
            db.add(record)

            score += 15
            messages.append(f"New {label} behavior detected: {key}")
            impact = "increase"

        else:
            record.count += 1
            record.last_seen = now

            if record.count < 5:
                score += 5
                messages.append(f"Rare {label} behavior: {key}")
                impact = "increase"
            else:
                messages.append(f"Known {label} behavior: {key}")

        db.commit()

    db.close()

    # Clean output
    if not messages:
        messages.append("No anomalous behavior detected")

    return score, "; ".join(messages), impact
