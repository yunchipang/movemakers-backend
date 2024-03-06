from pydantic import BaseModel, ConfigDict
from datetime import date, datetime, time
from typing import Optional

from ..enums.level import LevelEnum
from ..enums.style import StyleEnum


class TrainingBase(BaseModel):
    level: LevelEnum
    style: StyleEnum
    instructor: str
    description: Optional[str] = None
    date: date
    time: time
    duration: int = 60
    price: int = 18
    currency: str = 'USD'
    studio: str
    flyer: Optional[str] = None
    max_slots: int
    is_active: bool


class Training(TrainingBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CreateTraining(TrainingBase):
    pass