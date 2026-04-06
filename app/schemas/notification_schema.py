from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class NotificationCreate(BaseModel):
    user_id: str
    alert_id: str
    recipient_email: EmailStr
    message: str


class NotificationResponse(BaseModel):
    id: str
    user_id: str
    alert_id: str
    recipient_email: EmailStr
    status: str
    created_at: datetime