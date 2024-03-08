from pydantic import BaseModel, ConfigDict, UUID4
from datetime import date, datetime, time
from typing import List, Optional

from app.models.training import LevelEnum, StyleEnum


class TrainingBase(BaseModel):
    level: LevelEnum
    style: StyleEnum
    instructors: List[UUID4]
    description: Optional[str] = None
    date: date
    time: time
    duration: int = 60
    price: int = 18
    currency: str = "USD"
    studio: str
    flyer: Optional[str] = None
    max_slots: int
    is_active: bool


class Training(TrainingBase):
    id: UUID4
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CreateTraining(TrainingBase):
    pass
