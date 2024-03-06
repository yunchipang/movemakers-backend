from sqlalchemy import Column, Integer, String, Enum

from app.database import Base


class Dancer(Base):
    __tablename__ = "dancers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    bio = Column(String)
    based_in = Column(String)
    instagram_handle = Column(String, unique=True, index=True)
