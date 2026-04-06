from app.db.mongodb import database
from app.repositories.base_repo import BaseRepository

location_collection = database["locations"]


class LocationRepository(BaseRepository):

    @staticmethod
    async def add_location(location_data: dict):
        result = await location_collection.insert_one(location_data)
        return str(result.inserted_id)

    @staticmethod
    async def get_locations_by_alert(alert_id: str):
        locations = location_collection.find({"alert_id": alert_id})
        return BaseRepository.serialize([loc async for loc in locations])