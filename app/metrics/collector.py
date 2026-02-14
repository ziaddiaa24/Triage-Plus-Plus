from app.data.postgres import SessionLocal
from app.data.models import AlertMetrics

def increment(key):
    db = SessionLocal()
    record = db.get(AlertMetrics, key)

    if not record:
        record = AlertMetrics(key=key, count=1)
        db.add(record)
    else:
        record.count += 1

    db.commit()
    db.close()

def get_count(key):
    db = SessionLocal()
    record = db.get(AlertMetrics, key)
    db.close()
    return record.count if record else 0
