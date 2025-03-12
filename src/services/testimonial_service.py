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
def get_all_testimonials(db_session: Session) -> list[TestimonialResponse]:
    log.info("Getting all testimonials sorted by rating (desc)")

    try:
        testimonials = (
            db_session.query(TestimonialModel)
            .order_by(TestimonialModel.rating.desc())
            .all()
        )

        if not testimonials:
            log.info("No testimonials found")
            return []

        return [TestimonialResponse.from_orm(testimonial) for testimonial in testimonials]

    except OperationalError as e:
        log.error(f"Operational error while fetching testimonials: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Database error occurred")

    except Exception as e:
        log.error(f"Unexpected error while fetching testimonials: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@backoff.on_exception(
    backoff.expo,
    OperationalError,
    max_tries=3,
    on_backoff=backoff_handler
)
def create_testimonial(testimonial: TestimonialCreate, db_session: Session) -> TestimonialResponse:
    log.info("Creating a new testimonial")

    try:
        new_testimonial = TestimonialModel(
            first_name=testimonial.firstName,
            last_name=testimonial.lastName,
            rating=testimonial.rating,
            comment=testimonial.comment
        )
        db_session.add(new_testimonial)
        db_session.commit()
        db_session.refresh(new_testimonial)

        return TestimonialResponse.from_orm(new_testimonial)

    except OperationalError as e:
        db_session.rollback()
        log.error(f"Database error. Exception: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Database Error")

    except Exception as e:
        db_session.rollback()
        log.error(f"Error creating testimonial. Exception: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
