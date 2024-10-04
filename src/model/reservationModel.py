from pydantic import BaseModel


class ReservationModel(BaseModel):
    reservation_id: int = 123
    name: str = ""
    phoneNumber: str = ""
    email: str = ""
    insurance: str = ""
    message: str = ""
    date: str = ""
    hour: str = ""

