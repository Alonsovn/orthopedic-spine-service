from pydantic import BaseModel


class EmailSchema(BaseModel):
    from_user : str
    subject: str
    message: str
