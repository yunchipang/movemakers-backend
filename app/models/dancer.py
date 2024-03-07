from sqlalchemy import Column, Integer, String

from app.database import Base


# models data classes define teh SQL tables
# while schemas data classes define the API that FastAPI uses the interact with the database
class Dancer(Base):
    __tablename__ = "dancers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    instagram_handle = Column(String, unique=True)
    youtube_channel = Column(String(255), nullable=True)
    nationality = Column(String(255))
    bio = Column(String)
    based_in = Column(String(255))
