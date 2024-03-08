import uuid

from sqlalchemy import ARRAY, Column, Enum, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.database.database import Base
from app.database.associations import (
    crew_director_association,
    crew_captain_association,
    crew_member_association,
)
from .training import StyleEnum


class Crew(Base):
    __tablename__ = "crews"

    id = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
        nullable=False,
    )
    name = Column(String(255), index=True)
    bio = Column(Text)
    based_in = Column(String(255))
    founded_in = Column(Integer, nullable=True)
    styles = Column(ARRAY(Enum(StyleEnum, name="style_enum")))
    directors = relationship(
        "Dancer", secondary=crew_director_association, back_populates="director_of"
    )
    captains = relationship(
        "Dancer", secondary=crew_captain_association, back_populates="captain_of"
    )
    members = relationship(
        "Dancer", secondary=crew_member_association, back_populates="member_of"
    )
    rehearsal_schedules = Column(Text, nullable=True)
    instagram = Column(String(255), unique=True)
    youtube = Column(String(255), nullable=True)
    website = Column(String(255))
