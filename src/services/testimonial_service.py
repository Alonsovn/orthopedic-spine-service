import backoff
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.models.testimonial import TestimonialModel
from src.schemas.testimonial import TestimonialResponse, TestimonialCreate
from src.utils.backoff_helper import backoff_handler
from src.utils.logUtil import log


@backoff.on_exception(
    backoff.expo,  # Exponential backoff strategy
    OperationalError,  # Type of exception to retry on
    max_tries=3,  # Maximum retries
    on_backoff=backoff_handler  # Log or handle retry attempt
)
def get_all_testimonials(db: Session):
    log.info("Start fetching all testimonials sorted by rating in descending order")

    testimonials = db.query(TestimonialModel).order_by(TestimonialModel.rating.desc()).all()

    if not testimonials:
        return []

    return (TestimonialResponse.model_validate(testimonial) for testimonial in testimonials)


@backoff.on_exception(
    backoff.expo,
    OperationalError,
    max_tries=3,
    on_backoff=backoff_handler
)
def create_testimonial(testimonial: TestimonialCreate, db: Session):
    log.info("Start creating testimonial in db")

    try:
        new_testimonial = TestimonialModel(
            first_name=testimonial.firstName,
            last_name=testimonial.lastName,
            rating=testimonial.rating,
            comment=testimonial.comment
        )
        db.add(new_testimonial)
        db.commit()
        db.refresh(new_testimonial)

        return new_testimonial

    except OperationalError as e:
        db.rollback()
        log.error(f"Database error. Exception: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Database Error")

    except Exception as e:
        db.rollback()
        log.error(f"Error creating testimonial. Exception: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        db.close()
