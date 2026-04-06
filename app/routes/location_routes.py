from fastapi import APIRouter, Depends
from app.schemas.location_schema import LocationUpdate
from app.services.location_service import LocationService
from app.core.security import verify_token
from app.utils.response import success_response

router = APIRouter()


@router.post("/update")
async def update_location(data: LocationUpdate, user=Depends(verify_token)):
    result = await LocationService.update_location(data)
    return success_response(result, "Location updated")


@router.get("/{alert_id}")
async def get_locations(alert_id: str, user=Depends(verify_token)):
    result = await LocationService.get_alert_locations(alert_id)
    return success_response(result)