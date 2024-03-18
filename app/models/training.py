import uuid

from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Enum,
    Date,
    DateTime,
    Time,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base
from app.enums.level import Level
from app.enums.style import Style
from app.association import training_instructor_association


class Training(Base):
    __tablename__ = "trainings"

    id = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
        nullable=False,
    )
    created_at = Column(DateTime, default=datetime.utcnow)
    level = Column(Enum(Level))
    style = Column(Enum(Style))
    description = Column(String, nullable=True)
    date = Column(Date())
    time = Column(Time())
    duration = Column(Integer, default=60)
    price = Column(Integer, default=18)
    currency = Column(String, default="USD")
    flyer = Column(String, nullable=True)  # flyer is a URL to the image
    capacity = Column(Integer)
    is_active = Column(Boolean)

    studio_id = Column(UUID(as_uuid=True), ForeignKey("studios.id"), nullable=True)
    studio = relationship("Studio", back_populates="trainings")

    # relationship to the Dancer model
    instructors = relationship(
        "Dancer", secondary=training_instructor_association, back_populates="instructed_trainings"
    )

    def __repr__(self):
        """returns strings representation of model instance"""
        # instructor_names = ", ".join(
        #     [str(instructor) for instructor in self.instructors]
        # )
        # return "<Training level={!r}, style={!r}, instructors={!r}>".format(
        #     self.level, self.style, instructor_names
        # )
        return f"<Training {self.id!r}>"
