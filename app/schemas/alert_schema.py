from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# 🚨 ALERT TRIGGER

class AlertTrigger(BaseModel):
    user_id: str
    latitude: float
    longitude: float
    device_id: Optional[str] = None


# 🔁 ALERT STATUS

class AlertStatus(BaseModel):
    alert_id: str
    status: str  # active / resolved / cancelled


# 📤 RESPONSE

class AlertResponse(BaseModel):
    id: str
    user_id: str
    status: str
    latitude: float
    longitude: float
    created_at: datetime