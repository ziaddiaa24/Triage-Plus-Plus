from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from app.data.postgres import Base

class BehaviorEvent(Base):
    __tablename__ = "behavior_events"

    id = Column(String, primary_key=True)
    user = Column(String, index=True)
    source_ip = Column(String)
    asset = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

class RepetitionPattern(Base):
    __tablename__ = "repetition_patterns"

    fingerprint = Column(String, primary_key=True, index=True)
    count = Column(Integer, default=1)
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)

class BehaviorBaseline(Base):
    __tablename__ = "behavior_baseline"

    key = Column(String, primary_key=True)   # user+asset or ip+asset
    count = Column(Integer, default=1)
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)

class AlertMetrics(Base):
    __tablename__ = "alert_metrics"

    key = Column(String, primary_key=True)
    count = Column(Integer, default=0)

class TrainingSample(Base):
    __tablename__ = "training_samples"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base = Column(Integer)
    repetition = Column(Integer)
    behavior = Column(Integer)
    intel = Column(Integer)
    decision = Column(Integer)   # 1 = ESCALATE, 0 = SUPPRESS
