from app.db.mongodb import alert_collection
from app.repositories.base_repo import BaseRepository


class AlertRepository(BaseRepository):

    @staticmethod
    async def create_alert(alert_data: dict):
        result = await alert_collection.insert_one(alert_data)
        return str(result.inserted_id)

    @staticmethod
    async def get_by_id(alert_id: str):
        alert = await alert_collection.find_one({
            "_id": BaseRepository.to_objectid(alert_id)
        })
        return BaseRepository.serialize(alert) if alert else None

    @staticmethod
    async def update_status(alert_id: str, status: str):
        await alert_collection.update_one(
            {"_id": BaseRepository.to_objectid(alert_id)},
            {"$set": {"status": status}}
        )
        return await AlertRepository.get_by_id(alert_id)

    @staticmethod
    async def get_active_alerts_by_user(user_id: str):
        alerts = alert_collection.find({
            "user_id": user_id,
            "status": "active"
        })
        return BaseRepository.serialize([alert async for alert in alerts])

    @staticmethod
    async def get_all_alerts_by_user(user_id: str):
        alerts = alert_collection.find({
            "user_id": user_id
        }).sort("created_at", -1)
        return BaseRepository.serialize([alert async for alert in alerts])