from pydantic import BaseModel, Field
import uuid


class TestimonialCreate(BaseModel):
    firstName: str = Field(..., example="First name")
    lastName: str = Field(..., example="Last name")
    rating: int = Field(..., ge=1, le=5, example=5)
    comment: str = Field(..., example="Great service!")


class TestimonialResponse(TestimonialCreate):
    id: uuid.UUID

    class Config:
        from_attributes: True
