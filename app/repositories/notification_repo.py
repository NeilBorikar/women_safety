from app.db.mongodb import database
from app.repositories.base_repo import BaseRepository

notification_collection = database["notifications"]


class NotificationRepository(BaseRepository):

    @staticmethod
    async def create_notification(data: dict):
        result = await notification_collection.insert_one(data)
        return str(result.inserted_id)

    @staticmethod
    async def get_by_alert(alert_id: str):
        notifications = notification_collection.find({"alert_id": alert_id})
        return BaseRepository.serialize([n async for n in notifications])