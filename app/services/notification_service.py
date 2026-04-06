import asyncio
from app.utils.email import email_service
from app.utils.sms import sms_service
from app.models.notification_model import notification_model
from app.repositories.notification_repo import NotificationRepository


class NotificationService:

    # 🧠 Centralized message builder
    @staticmethod
    def build_message(user_name, location):
        return f"""
🚨 EMERGENCY ALERT 🚨

{user_name} may be in danger!

📍 Location:
https://maps.google.com/?q={location['latitude']},{location['longitude']}

Please act immediately.
"""

    # 📧 EMAIL SENDER
    @staticmethod
    async def send_email(user_id, alert_id, email, message):
        status = "sent"

        try:
            email_service.send_email(email, "🚨 EMERGENCY ALERT", message)
        except Exception:
            status = "failed"

        # 🧾 Log
        notification_data = notification_model({
            "user_id": user_id,
            "alert_id": alert_id,
            "recipient_email": email,
            "message": message
        })
        notification_data["channel"] = "email"
        notification_data["status"] = status

        await NotificationRepository.create_notification(notification_data)

    # 📱 SMS SENDER
    @staticmethod
    async def send_sms(user_id, alert_id, phone, message):
        status = "sent"

        try:
            sms_service.send_sms(phone, message)
        except Exception:
            status = "failed"

        # 🧾 Log
        notification_data = notification_model({
            "user_id": user_id,
            "alert_id": alert_id,
            "recipient_email": phone,
            "message": message
        })
        notification_data["channel"] = "sms"
        notification_data["status"] = status

        await NotificationRepository.create_notification(notification_data)

    # 🚀 MAIN NOTIFIER (PARALLEL + ROBUST)
    @staticmethod
    async def notify_contacts(user, alert_id, location):
        contacts = user.get("emergency_contacts", [])
        message = NotificationService.build_message(user["name"], location)

        tasks = []

        for contact in contacts:

            # 📧 Email
            if contact.get("email"):
                tasks.append(
                    NotificationService.send_email(
                        user["id"],
                        alert_id,
                        contact["email"],
                        message
                    )
                )

            # 📱 SMS
            if contact.get("phone"):
                tasks.append(
                    NotificationService.send_sms(
                        user["id"],
                        alert_id,
                        contact["phone"],
                        message
                    )
                )

        # ⚡ Run all notifications in parallel
        await asyncio.gather(*tasks, return_exceptions=True)