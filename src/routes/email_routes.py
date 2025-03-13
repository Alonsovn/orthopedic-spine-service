import os
import smtplib

from fastapi import APIRouter
from email.mime.text import MIMEText

from src.core.app_config import AppConfig
from src.schemas.email import EmailSchema
from src.utils.logUtil import log

router = APIRouter()

email_config: dict = AppConfig().config.get("email")

# Email configuration
SMTP_SERVER = email_config.get("smtpServer")
SMTP_PORT = email_config.get("smtpPort")
EMAIL_USERNAME = email_config.get("address")
EMAIL_PASSWORD = email_config.get("password")


@router.post("/send-email")
async def send_email(payload: EmailSchema):
    try:
        msg = MIMEText(payload.message)
        msg["Subject"] = payload.subject
        msg["From"] = payload.fromUser
        msg["To"] = EMAIL_USERNAME

        log.info(f"Email: {msg}")

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.send_message(msg)

        log.info("Email sent successfully")

        return {"message": "Email sent successfully"}

    except Exception as e:
        log.info(f"Error sending email. Exception: {e}")
