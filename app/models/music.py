import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class Music(Base):
    __tablename__ = "music"

    id = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
        nullable=False,
    )
    spotify_track_id = Column(String, nullable=False, unique=True)  # Spotify track ID, unique and non-nullable
    name = Column(String, nullable=False)
    artist = Column(String, nullable=False)
    album = Column(String, nullable=True)

    def __repr__(self):
        return f"<Music {self.name} by {self.artist}>"