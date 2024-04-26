import uuid

from sqlalchemy import Boolean, Column, LargeBinary, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base
from app.settings import get_settings


settings = get_settings()


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
        nullable=False,
    )
    username = Column(String(225), nullable=False, unique=True)
    email = Column(String(225), nullable=False, unique=True)
    first_name = Column(String(225), nullable=True)
    last_name = Column(String(225), nullable=True)
    hashed_password = Column(LargeBinary, nullable=False)
    disabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())

    registered_trainings = relationship(
        "Training", secondary="training_registration", back_populates="participants"
    )

    def __repr__(self):
        """returns strings representation of model instance"""
        return "<User {email!r}>".format(email=self.email)
