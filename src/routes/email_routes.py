import os
import smtplib

from fastapi import APIRouter
from email.mime.text import MIMEText

from src.schemas.email import EmailSchema
from src.utils.logUtil import log

router = APIRouter()

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")  # Your Gmail address
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  #


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
