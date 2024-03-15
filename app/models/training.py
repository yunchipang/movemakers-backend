import uuid

from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    Enum,
    Date,
    DateTime,
    Time,
    ARRAY,
)
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from app.database import Base
from app.enums.level import Level
from app.enums.style import Style


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
    instructor_ids = Column(ARRAY(UUID(as_uuid=True)))
    description = Column(String, nullable=True)
    date = Column(Date())
    time = Column(Time())
    duration = Column(Integer, default=60)
    price = Column(Integer, default=18)
    currency = Column(String, default="USD")
    studio_id = Column(UUID(as_uuid=True))
    flyer = Column(String, nullable=True)  # flyer is a URL to the image
    max_slots = Column(Integer)
    is_active = Column(Boolean)

    class Config:
        orm_mode = True

    def __repr__(self):
        """returns strings representation of model instance"""
        # instructor_names = ", ".join(
        #     [str(instructor) for instructor in self.instructors]
        # )
        # return "<Training level={!r}, style={!r}, instructors={!r}>".format(
        #     self.level, self.style, instructor_names
        # )
        return "<Training {id!r}>".format(id=self.id)
