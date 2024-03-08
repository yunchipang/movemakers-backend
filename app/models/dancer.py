import uuid

from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.database.database import Base
from app.database.associations import (
    crew_director_association,
    crew_captain_association,
    crew_member_association,
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
    director_of = relationship(
        "Crew", secondary=crew_director_association, back_populates="directors"
    )
    captain_of = relationship(
        "Crew", secondary=crew_captain_association, back_populates="captains"
    )
    member_of = relationship(
        "Crew", secondary=crew_member_association, back_populates="members"
    )
    owner_of = relationship(
        "Studio", secondary=studio_owner_association, back_populates="owners"
    )
    instructor_of = relationship(
        "Training", secondary=training_instructor_association, back_populates="instructors"
    )
