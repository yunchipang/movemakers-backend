import uuid

from sqlalchemy import ARRAY, Column, Enum, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID

from app.database.database import Base
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
    home_studio_id = Column(UUID(as_uuid=True))
    styles = Column(ARRAY(Enum(StyleEnum, name="style_enum")))
    director_ids = Column(ARRAY(UUID(as_uuid=True)))
    captain_ids = Column(ARRAY(UUID(as_uuid=True)))
    member_ids = Column(ARRAY(UUID(as_uuid=True)))
    rehearsal_schedules = Column(Text, nullable=True)
    instagram = Column(String(255), unique=True)
    youtube = Column(String(255), nullable=True)
    website = Column(String(255))

    def __repr__(self):
        """returns strings representation of model instance"""
        return "<Crew {name!r}>".format(name=self.name)
