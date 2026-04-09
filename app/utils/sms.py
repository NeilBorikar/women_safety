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
            # 🌍 Format number for Twilio (ensure it starts with +)
            final_phone = str(phone).strip()
            if not final_phone.startswith('+'):
                if len(final_phone) == 10:
                    final_phone = f"+91{final_phone}"
                else:
                    final_phone = f"+{final_phone}"
            
            print(f"DEBUG: Twilio sending to: {final_phone}")

            message = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=final_phone
            )
            return message.sid

        except Exception as e:
            raise Exception(f"SMS failed: {str(e)}")


sms_service = SMSService()