from typing import List
from fastapi import APIRouter, status, Depends, HTTPException

from src.database.postgres import get_db
from src.schemas.testimonial import TestimonialCreate, TestimonialResponse
from sqlalchemy.orm import Session

from src.dependencies.auth_dependency import get_current_user
from src.services.testimonial_service import TestimonialService
from src.utils.logUtil import log

router = APIRouter()


@router.get("/all", response_model=List[TestimonialResponse])
async def fetch_all_testimonials(db_session: Session = Depends(get_db)):
    testimonial_service = TestimonialService()

    return testimonial_service.get_all_testimonials(db_session)


@router.post("/", response_model=TestimonialResponse, status_code=status.HTTP_201_CREATED)
async def add_testimonial(testimonial: TestimonialCreate, db_session: Session = Depends(get_db),
                          current_user: str = Depends(get_current_user)):
    testimonial_service = TestimonialService()

    return testimonial_service.create_testimonial(testimonial, db_session)


@router.delete("/{testimonial_id}")
async def delete_testimonial(testimonial_id: str, db_session: Session = Depends(get_db),
                             current_user: str = Depends(get_current_user)):
    testimonial_service = TestimonialService()
    deleted_testimonial = testimonial_service.delete_testimonial(testimonial_id, db_session)

    if not deleted_testimonial:
        return HTTPException(status_code=404, detail=f"Not testimonial with id {testimonial_id} found")
