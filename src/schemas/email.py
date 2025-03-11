from pydantic import BaseModel


class EmailSchema(BaseModel):
    fromUser: str
    subject: str
    message: str
