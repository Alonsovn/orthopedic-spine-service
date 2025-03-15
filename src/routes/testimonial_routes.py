from typing import List
from fastapi import APIRouter, status, Depends, HTTPException

from src.database.postgres import get_db
from src.schemas.testimonial import TestimonialCreate, TestimonialResponse
from sqlalchemy.orm import Session

from src.dependencies.auth_dependency import get_current_user
from src.services.testimonial_service import get_all_testimonials, create_testimonial

router = APIRouter()


@router.get("/all", response_model=List[TestimonialResponse])
async def fetch_all_testimonials(db_session: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    testimonials = get_all_testimonials(db_session)

    if not testimonials:
        raise HTTPException(status_code=404, detail="No testimonials found ...")

    return testimonials


@router.post("/", response_model=TestimonialResponse, status_code=status.HTTP_201_CREATED)
async def add_testimonial(testimonial: TestimonialCreate, db_session: Session = Depends(get_db),
                          current_user: str = Depends(get_current_user)):
    try:
        return create_testimonial(testimonial, db_session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating testimonial: {str(e)}")
