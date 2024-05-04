import uuid

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.association import (
    training_instructor_association,
    training_registration_association,
)
from app.database import Base
from app.enums.level import Level
from app.enums.style import Style

from app.utils.formatting import format_instructors


class Training(Base):
    __tablename__ = "trainings"

    id = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
        nullable=False,
    )
    created_at = Column(DateTime, default=func.now())
    level = Column(Enum(Level))
    style = Column(Enum(Style))
    description = Column(Text, nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    price = Column(Integer, default=18)
    currency = Column(String, default="USD")
    flyer = Column(String, nullable=True)  # flyer is a URL to the image
    max_slots = Column(Integer)
    is_active = Column(Boolean, nullable=True, default=True)

    studio_id = Column(UUID(as_uuid=True), ForeignKey("studios.id"), nullable=False)
    studio = relationship("Studio", back_populates="trainings")
    instructors = relationship(
        "Dancer",
        secondary=training_instructor_association,
        back_populates="instructed_trainings",
    )
    participants = relationship(
        "User",
        secondary=training_registration_association,
        back_populates="registered_trainings",
    )

    def __repr__(self):
        """returns strings representation of model instance"""
        instructors_string = format_instructors(self.instructors)
        return f"<Training {self.id}: {self.level.value} {self.style.value} w/ {instructors_string}>"
