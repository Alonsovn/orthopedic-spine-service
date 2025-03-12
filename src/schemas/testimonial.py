from pydantic import BaseModel, Field, model_validator
import uuid
from datetime import datetime


class TestimonialCreate(BaseModel):
    firstName: str = Field(..., max_length=255, example="First name")
    lastName: str = Field(..., max_length=255, example="Last name")
    rating: int = Field(..., ge=1, le=5, example=5)
    comment: str = Field(..., max_length=1000, example="Great service!")


class TestimonialResponse(BaseModel):
    id: uuid.UUID
    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")
    rating: int
    comment: str
    created_at: str = Field(..., alias="createdAt")
    updated_at: str = Field(..., alias="UpdatedAt")

    @model_validator(mode="before")
    def validate_dates(cls, values):
        # Ensure datetime fields are converted to string
        if 'created_at' in values and isinstance(values['created_at'], datetime):
            values['created_at'] = values['created_at'].isoformat()  # Convert to string
        if 'updated_at' in values and isinstance(values['updated_at'], datetime):
            values['updated_at'] = values['updated_at'].isoformat()  # Convert to string
        return values

    class Config:
        from_attributes = True
        populate_by_name = True  # Maps snake_case to camelCase when needed
