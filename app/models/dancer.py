import uuid

from sqlalchemy import Column, Date, Enum, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base
from app.association import studio_owner_association, training_instructor_association
from app.enums.pronouns import Pronouns


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
    pronouns = Column(Enum(Pronouns), nullable=True)
    bio = Column(Text)
    date_of_birth = Column(Date, nullable=True)
    nationality = Column(String(255))
    based_in = Column(String(255))
    instagram = Column(String, unique=True)
    youtube = Column(String(255), nullable=True)
    agency = Column(String(255), nullable=True)
    contact_email = Column(String(255), nullable=True)

    owned_studios = relationship(
        "Studio", secondary=studio_owner_association, back_populates="owners"
    )
    instructed_trainings = relationship(
        "Training",
        secondary=training_instructor_association,
        back_populates="instructors",
    )

    def __repr__(self):
        """returns strings representation of model instance"""
        return "<Dancer {name!r}>".format(name=self.name)
