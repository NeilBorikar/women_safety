from twilio.rest import Client
from app.core.config import settings


class SMSService:

    def __init__(self):
        self.client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN
        )
        self.from_number = settings.TWILIO_PHONE_NUMBER

    def send_sms(self, phone: str, message: str):
        try:
            message = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=phone
            )
            return message.sid

        except Exception as e:
            raise Exception(f"SMS failed: {str(e)}")


sms_service = SMSService()