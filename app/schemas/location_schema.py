from pydantic import BaseModel
from datetime import datetime


class LocationUpdate(BaseModel):
    alert_id: str
    latitude: float
    longitude: float
    timestamp: datetime