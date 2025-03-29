import backoff
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.models.testimonial import TestimonialModel
from src.schemas.testimonial import TestimonialResponse, TestimonialCreate
from src.utils.backoff_helper import backoff_handler
from src.utils.logUtil import log


class TestimonialService:

    @backoff.on_exception(backoff.expo, OperationalError, max_tries=3, on_backoff=backoff_handler)
    def get_all_testimonials(self, db_session: Session) -> list[TestimonialResponse]:
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

    @backoff.on_exception(backoff.expo, OperationalError, max_tries=3, on_backoff=backoff_handler)
    def create_testimonial(self, testimonial: TestimonialCreate, db_session: Session) -> TestimonialResponse:
        log.info("Creating a new testimonial")

        try:
            new_testimonial = TestimonialModel(
                first_name=testimonial.first_name,
                last_name=testimonial.last_name,
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

    @backoff.on_exception(backoff.expo, OperationalError, max_tries=3, on_backoff=backoff_handler)
    def delete_testimonial(self, testimonial_id: str, db_session: Session) -> bool:
        log.info(f"Deleting testimonial with id: {testimonial_id}")

        try:

            testimonial_db = db_session.query(TestimonialModel).filter(TestimonialModel.id == testimonial_id).one_or_none()

            if not testimonial_db:
                log.warning(f"Testimonial with id: {testimonial_id} not found")
                return False

            db_session.delete(testimonial_db)
            db_session.commit()

            return True

        except OperationalError as e:
            db_session.rollback()
            log.error(f"Database error. Exception: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Database Error")

        except Exception as e:
            db_session.rollback()
            log.error(f"Error creating testimonial. Exception: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Internal Server Error")
