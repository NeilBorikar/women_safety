from app.repositories.location_repo import LocationRepository
from app.models.location_model import location_model


class LocationService:

    @staticmethod
    async def update_location(location_data):
        location_dict = location_data.dict()

        new_location = location_model(location_dict)

        location_id = await LocationRepository.add_location(new_location)

        return {
            "location_id": location_id
        }

    @staticmethod
    async def get_alert_locations(alert_id: str):
        return await LocationRepository.get_locations_by_alert(alert_id)