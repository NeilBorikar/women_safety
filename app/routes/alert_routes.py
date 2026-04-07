from fastapi import APIRouter, Depends
from app.schemas.alert_schema import AlertTrigger
from app.services.alert_service import AlertService
from app.core.security import verify_token
from app.utils.response import success_response

router = APIRouter()


@router.post("/trigger")
async def trigger_alert(data: AlertTrigger, user=Depends(verify_token)):
    result = await AlertService.trigger_alert(data)
    return success_response(result, "Alert triggered")


@router.post("/resolve/{alert_id}")
async def resolve_alert(alert_id: str, user=Depends(verify_token)):
    result = await AlertService.resolve_alert(alert_id)
    return success_response(result, "Alert resolved")


@router.get("/all")
async def get_all_alerts(user=Depends(verify_token)):
    result = await AlertService.get_user_alerts(user["user_id"])
    return success_response(result)