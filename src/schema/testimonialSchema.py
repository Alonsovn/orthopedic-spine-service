from pydantic import BaseModel, Field


class TestimonialCreate(BaseModel):
    firstName: str = Field(..., example="First name")
    lastName: str = Field(..., example="Last name")
    rating: int = Field(..., ge=1, le=5, example=5)
    testimony: str = Field(..., example="Great service!")


class TestimonialResponse(TestimonialCreate):
    id: int
