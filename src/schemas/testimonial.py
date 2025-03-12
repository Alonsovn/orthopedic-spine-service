from pydantic import BaseModel, Field, model_validator
import uuid
from datetime import datetime

from src.models.testimonial import TestimonialModel


class TestimonialCreate(BaseModel):
    first_name: str = Field(..., alias="firstName", max_length=255, example="First name")
    last_name: str = Field(..., alias="lastName", max_length=255, example="Last name")
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
    def validate_dates(cls, obj):
        if isinstance(obj, TestimonialModel):  # Ensure we have a model instance
            return {
                "id": obj.id,
                "first_name": obj.first_name,
                "last_name": obj.last_name,
                "rating": obj.rating,
                "comment": obj.comment,
                "created_at": obj.created_at.isoformat() if obj.created_at else None,
                "updated_at": obj.updated_at.isoformat() if obj.updated_at else None,
            }
        return obj  # If obj is already a dict, return as is

    class Config:
        from_attributes = True
        populate_by_name = True  # Maps snake_case to camelCase when needed
