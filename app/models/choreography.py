import uuid

from sqlalchemy import ARRAY, Column, DateTime, Enum, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.association import (
    choreography_choreographer_association,
    choreography_music_association,
)
from app.database import Base
from app.enums.level import Level
from app.enums.style import Style


class Choreography(Base):
    __tablename__ = "choreographies"

    id = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
        nullable=False,
    )
    created_at = Column(DateTime, default=func.now())
    description = Column(Text, nullable=True)
    level = Column(Enum(Level))
    styles = Column(ARRAY(Enum(Style)))
    video_urls = Column(ARRAY(String), nullable=True)
    
    choreographers = relationship("Dancer", secondary=choreography_choreographer_association, back_populates="choreographies")
    music = relationship("Music", secondary=choreography_music_association, back_populates="choreographies")

    def __repr__(self):
        """returns strings representation of model instance"""
        choreographer_names = ", ".join([choreographer.name for choreographer in self.choreographers])
        return f"<{self.music_spotify_track_id}> by {choreographer_names}"