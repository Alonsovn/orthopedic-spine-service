from pydantic import BaseModel
import uuid


class ReservationModel(BaseModel):
    reservation_id: uuid.UUID
    name: str = ""
    phoneNumber: str = ""
    email: str = ""
    insurance: str = ""
    message: str = ""
    date: str = ""
    hour: str = ""

