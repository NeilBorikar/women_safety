from app.repositories.alert_repo import AlertRepository
from app.repositories.user_repo import UserRepository
from app.models.alert_model import alert_model
from app.services.notification_service import NotificationService
from app.utils.exceptions import NotFoundException


class AlertService:

    @staticmethod
    async def trigger_alert(alert_data):
        # 👤 Validate user
        user = await UserRepository.get_by_id(alert_data.user_id)

        if not user:
            raise NotFoundException("User not found")

        # 🚨 Create alert
        alert_dict = alert_data.dict()
        new_alert = alert_model(alert_dict)

        alert_id = await AlertRepository.create_alert(new_alert)

        # 📧 Notify contacts (ASYNC SIDE EFFECT)
        location = {
            "latitude": alert_data.latitude,
            "longitude": alert_data.longitude
        }

        await NotificationService.notify_contacts(
            user.get("emergency_contacts", []),
            user["name"],
            location
        )

        return {
            "alert_id": alert_id,
            "status": "active",
            "message": "Emergency alert triggered"
        }

    @staticmethod
    async def resolve_alert(alert_id: str):
        alert = await AlertRepository.get_by_id(alert_id)

        if not alert:
            raise NotFoundException("Alert not found")

        updated = await AlertRepository.update_status(alert_id, "resolved")

        return {
            "alert_id": alert_id,
            "status": updated["status"]
        }

    @staticmethod
    async def get_user_alerts(user_id: str):
        alerts = await AlertRepository.get_all_alerts_by_user(user_id)
        return alerts