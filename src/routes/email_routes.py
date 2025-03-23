
from fastapi import APIRouter, status, HTTPException

from src.schemas.email import EmailSchema
from src.services.emai_service import EmailService
from src.utils.logUtil import log

router = APIRouter()


@router.post("/receive-email", status_code=status.HTTP_201_CREATED)
async def receive_email(email_payload: EmailSchema):
    email_service = EmailService()
    email_service.receive_email_from_client(email_payload)

    return {"success": "Email received successfully"}


@router.post("/send-verification-code-email", status_code=status.HTTP_200_OK)
async def send_verification_code_email(email: str):
    if not email:
        log.error("Missing email parameter")
        raise HTTPException(status_code=500, detail="Verification error: Could not send the verification code")

    email_service = EmailService()
    verification_code = email_service.send_code_verification_email(email)

    return {"verificationCode": verification_code}
