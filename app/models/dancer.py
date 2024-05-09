import uuid

from sqlalchemy import Column, Date, Enum, LargeBinary, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.association import (
    choreography_choreographer_association,
    crew_leader_association,
    crew_member_association,
    studio_owner_association,
    training_instructor_association,
)
from app.database import Base
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
    image_url = Column(String(500), nullable=True)
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
    leading_crews = relationship(
        "Crew", secondary=crew_leader_association, back_populates="leaders"
    )
    member_of_crews = relationship(
        "Crew", secondary=crew_member_association, back_populates="members"
    )
    choreos = relationship(
        "Choreography",
        secondary=choreography_choreographer_association,
        back_populates="choreographers",
    )

    def __repr__(self):
        """returns strings representation of model instance"""
        return "<Dancer: {name!r}>".format(name=self.name)
