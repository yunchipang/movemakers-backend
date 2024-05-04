import uuid

from sqlalchemy import ARRAY, Column, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.association import (
    choreography_choreographer_association,
)
from app.database import Base
from app.enums.level import Level
from app.enums.style import Style
from app.utils.formatting import format_dancers


class Choreography(Base):
    __tablename__ = "choreos"

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
    videos = Column(ARRAY(String))  # stores a list of video links

    # fk to the dancer table
    choreographers = relationship(
        "Dancer",
        secondary=choreography_choreographer_association,
        back_populates="choreos",
    )
    # fk to the music table
    music_id = Column(String, ForeignKey("music.spotify_track_id"))
    music = relationship("Music", back_populates="choreos")

    def __repr__(self):
        choreographer_names = format_dancers(self.choreographers)
        music_name = self.music.name
        music_artist = self.music.artist
        return f"<Choreography {self.id}: {music_name} by {music_artist} choreographed by {choreographer_names}>"
