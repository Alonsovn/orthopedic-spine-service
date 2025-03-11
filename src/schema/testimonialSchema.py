from pydantic import BaseModel, Field
import uuid


class TestimonialCreate(BaseModel):
    firstName: str = Field(..., example="First name")
    lastName: str = Field(..., example="Last name")
    rating: int = Field(..., ge=1, le=5, example=5)
    comment: str = Field(..., example="Great service!")


class TestimonialResponse(BaseModel):
    id: uuid.UUID
    firstName: str = Field(..., alias="first_name")
    lastName: str = Field(..., alias="last_name")
    rating: int
    comment: str

    class Config:
        from_attributes = True
        populate_by_name = True  # Allows FastAPI to map snake_case from DB
