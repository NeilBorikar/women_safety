from fastapi import APIRouter, Depends
from app.schemas.evidence_schema import EvidenceUpload
from app.services.evidence_service import EvidenceService
from app.core.security import verify_token
from app.utils.response import success_response

router = APIRouter()


@router.post("/upload")
async def upload_evidence(data: EvidenceUpload, user=Depends(verify_token)):
    result = await EvidenceService.upload_evidence(data)
    return success_response(result, "Evidence uploaded")


@router.get("/{alert_id}")
async def get_evidence(alert_id: str, user=Depends(verify_token)):
    result = await EvidenceService.get_evidence(alert_id)
    return success_response(result)