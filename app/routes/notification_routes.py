from fastapi import APIRouter, Depends
from app.repositories.notification_repo import NotificationRepository
from app.core.security import verify_token
from app.utils.response import success_response

router = APIRouter()


@router.get("/{alert_id}")
async def get_notifications(alert_id: str, user=Depends(verify_token)):
    result = await NotificationRepository.get_by_alert(alert_id)
    return success_response(result)