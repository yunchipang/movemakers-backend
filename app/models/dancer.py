import uuid

from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.database.database import Base
from app.database.associations import (
    studio_owner_association,
    training_instructor_association,
)


# models data classes define teh SQL tables
# while schemas data classes define the API that FastAPI uses the interact with the database
class Dancer(Base):
    __tablename__ = "dancers"

    id = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
        nullable=False,
    )
    name = Column(String(255), index=True)
    bio = Column(Text)
    nationality = Column(String(255))
    based_in = Column(String(255))
    instagram = Column(String, unique=True)
    youtube = Column(String(255), nullable=True)

    # reverse relationships
    owner_of = relationship(
        "Studio", secondary=studio_owner_association, back_populates="owners"
    )
    instructor_of = relationship(
        "Training",
        secondary=training_instructor_association,
        back_populates="instructors",
    )

    def __repr__(self):
        """returns strings representation of model instance"""
        return "<Dancer {name!r}>".format(name=self.name)
