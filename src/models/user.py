from src.database.postgres import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

from sqlalchemy import Column, String, Boolean


class UserModel(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String(255))
    email = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    isAdmin = Column(Boolean, nullable=False, default=False)
    isActive = Column(Boolean, nullable=False, default=True)
