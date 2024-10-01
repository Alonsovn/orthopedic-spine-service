from pydantic import BaseModel


class ReservationModel(BaseModel):
    reservation_id: int = 123
    name: str = ""
    email: str = ""
    message: str = ""

    def __init__(self, reservation_id: int, name: str, email: str, message: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reservation_id = reservation_id
        self.name = name
        self.email = email
        self.message = message
