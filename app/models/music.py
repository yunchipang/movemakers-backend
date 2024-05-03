from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.database import Base


class Music(Base):
    __tablename__ = "music"

    spotify_track_id = Column(
        String, primary_key=True, unique=True, nullable=False
    )  # Spotify track ID as primary key
    name = Column(String, nullable=False)
    artist = Column(String, nullable=False)

    # fk to the choreos table
    choreos = relationship("Choreography", back_populates="music")

    def __repr__(self):
        return "<Music: {name!r} by {artist!r}>".format(
            name=self.name, artist=self.artist
        )
