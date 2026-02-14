from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class AlertIn(BaseModel):
    alert_id: Optional[str] = None
    rule_name: Optional[str] = "unknown_rule"
    severity: Optional[str] = "MEDIUM"

    source_ip: Optional[str] = "0.0.0.0"
    destination: Optional[str] = "unknown"

    user: Optional[str] = "unknown"
    asset: Optional[str] = "unknown"

    timestamp: Optional[datetime] = None
