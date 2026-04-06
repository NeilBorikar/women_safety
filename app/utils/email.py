import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings


class EmailService:
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.email = settings.EMAIL
        self.password = settings.EMAIL_PASSWORD

    def send_email(self, to_email: str, subject: str, body: str):
        try:
            msg = MIMEMultipart()
            msg["From"] = self.email
            msg["To"] = to_email
            msg["Subject"] = subject

            msg.attach(MIMEText(body, "plain"))

            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.email, self.password)
                server.send_message(msg)

        except Exception as e:
            raise Exception(f"Email sending failed: {str(e)}")


# Singleton instance (important pattern)
email_service = EmailService()