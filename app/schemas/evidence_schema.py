from pydantic import BaseModel
from typing import Optional


class EvidenceUpload(BaseModel):
    alert_id: str
    file_type: str  # audio / image / video
    file_url: str
    timestamp: Optional[str] = None