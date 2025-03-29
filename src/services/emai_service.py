import random

from src.core.app_config import AppConfig
from src.schemas.email import EmailSchema
from email.mime.text import MIMEText
import smtplib

from src.utils.logUtil import log

email_config: dict = AppConfig().config.get("email")


class EmailService:

    def __init__(self):
        self.smtp_server = email_config.get("smtpServer", "smtp.gmail.com")
        self.smtp_port = email_config.get("smtpPort", 465)
        self.email_address = email_config.get("address", "orthopedicspineinfo@gmail.com")
        self.email_password = email_config.get("password", "")

    def send_email(self, email_content: MIMEText):
        log.info(f"Sending email: {email_content}")

        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.email_address, self.email_password)
                server.send_message(email_content)
            log.info("Email sent successfully")

            return True

        except Exception as e:
            log.info(f"Error sending email. Exception: {e}")

    def receive_email_from_client(self, email_payload: EmailSchema):

        try:

            email_message = MIMEText(email_payload.message)
            email_message["Subject"] = f"Mensaje de: {email_payload.subject}"
            email_message["From"] = email_payload.fromUser
            email_message["To"] = self.email_address

            self.send_email(email_message)

            return {"success": "Email sent successfully"}

        except Exception as e:
            log.info(f"Error sending email. Exception: {e}")

    def send_code_verification_email(self, email_to: str):
        log.info(f"Sending verification code to: {email_to}")

        try:

            verification_code = self.generate_verification_code()
            message = f"Este es tu número de verificación: {verification_code}"

            email_message = MIMEText(message)
            email_message["Subject"] = "Código de verificación"
            email_message["From"] = self.email_address
            email_message["To"] = email_to

            log.info("Code verification email sent successfully")
            self.send_email(email_message)

            return verification_code

        except Exception as e:
            log.info(f"Error sending verification code email. Exception: {str(e)}")

    @staticmethod
    def generate_verification_code():
        return random.randint(1000, 9999)
