from sqlalchemy import Column, String

from app.database import Base


class Music(Base):
    __tablename__ = "music"

    spotify_track_id = Column(
        String, primary_key=True, unique=True, nullable=False
    )  # Spotify track ID as primary key
    name = Column(String, nullable=False)
    artist = Column(String, nullable=False)

    def __repr__(self):
        return f"<Music {self.name} by {self.artist}>"
