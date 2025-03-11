from typing import List
from fastapi import APIRouter, status, Depends, HTTPException

from src.database.postgres import get_db
from src.schemas.testimonial import TestimonialCreate, TestimonialResponse
from src.services.testimonial_service import get_all_testimonials, create_testimonial
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/all", response_model=List[TestimonialResponse])
async def fetch_all_testimonials(db: Session = Depends(get_db)):
    return get_all_testimonials(db)


@router.post("/", response_model=TestimonialResponse, status_code=status.HTTP_201_CREATED)
async def add_testimonial(testimonial: TestimonialCreate, db: Session = Depends(get_db)):
    return create_testimonial(testimonial, db)
