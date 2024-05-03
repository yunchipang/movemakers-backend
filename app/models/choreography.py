# import uuid

# from sqlalchemy import ARRAY, Column, DateTime, Enum, String, Text
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql import func

# from app.association import (
#     choreography_choreographer_association,
#     choreography_music_association,
# )
# from app.database import Base
# from app.enums.level import Level
# from app.enums.style import Style


# class Choreography(Base):
#     __tablename__ = "choreos"

#     id = Column(
#         UUID(as_uuid=True),
#         default=uuid.uuid4,
#         primary_key=True,
#         unique=True,
#         nullable=False,
#     )
#     created_at = Column(DateTime, default=func.now())
#     description = Column(Text, nullable=True)
#     level = Column(Enum(Level))
#     styles = Column(ARRAY(Enum(Style)))
#     video_urls = Column(ARRAY(String), nullable=True)

#     choreographers = relationship(
#         "Dancer",
#         secondary=choreography_choreographer_association,
#         back_populates="choreos",
#     )
#     music = relationship(
#         "Music",
#         secondary=choreography_music_association,
#         back_populates="choreos",
#     )

#     def __repr__(self):
#         choreographer_names = ", ".join(
#             choreographer.name for choreographer in self.choreographers
#         )
#         music_name = self.music.name
#         music_artist = self.music.artist
#         return f"<Choreography {self.id}, {music_name} by {music_artist} choreographed by {choreographer_names}>"
