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
        
        print(f"DEBUG: Notifying {len(contacts)} contacts for user {user.get('name')}")
        
        message = NotificationService.build_message(user.get("name", "Someone"), location)

        tasks = []

        for contact in contacts:
            contact_name = contact.get("name", "Contact")
            phone = contact.get("phone")
            email = contact.get("email")

            print(f"DEBUG: Processing contact {contact_name} (Phone: {phone}, Email: {email})")

            # 📧 Email
            if email:
                tasks.append(
                    NotificationService.send_email(
                        user["id"],
                        alert_id,
                        email,
                        message
                    )
                )

            # 📱 SMS
            if phone:
                tasks.append(
                    NotificationService.send_sms(
                        user["id"],
                        alert_id,
                        phone,
                        message
                    )
                )

        if not tasks:
            print("DEBUG: No valid notification tasks found (contacts might be missing phone/email)")

        # ⚡ Run all notifications in parallel
        await asyncio.gather(*tasks, return_exceptions=True)
        print("DEBUG: All notification tasks completed.")