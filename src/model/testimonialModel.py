import uuid
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import Column, Integer, String, DateTime, func

from src.database.postgresSql import Base


class TestimonialModel(Base):
    __tablename__ = "testimonial"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
