from sqlalchemy import Column, Integer, String

from app.database import Base


class Studio(Base):
    __tablename__ = "studios"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    address = Column(String)
    email = Column(String(255))
    phone = Column(String(255))
    opening_hours = Column(String)
    website = Column(String(255))
    owner = Column(String, nullable=True)
    room_count = Column(Integer, nullable=True)
    since = Column(Integer, nullable=True)
