from sqlalchemy import Boolean, Column, Integer, String, Enum, Date, DateTime, Time
from datetime import datetime

from app.database import Base
from ..enums.level import LevelEnum
from ..enums.style import StyleEnum


class Training(Base):
    __tablename__ = "trainings"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    level = Column(Enum(LevelEnum))
    style = Column(Enum(StyleEnum))
    instructor = Column(String)
    description = Column(String, nullable=True)
    date = Column(Date())
    time = Column(Time())
    duration = Column(Integer, default=60)
    price = Column(Integer, default=18)
    currency = Column(String, default='USD')
    studio = Column(String)
    flyer =  Column(String, nullable=True) # flyer is a URL to the image
    max_slots = Column(Integer)
    is_active = Column(Boolean)

    class Config:
        orm_mode = True