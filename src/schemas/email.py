from pydantic import BaseModel, EmailStr


class EmailSchema(BaseModel):
    fromUser: EmailStr
    subject: str
    message: str
