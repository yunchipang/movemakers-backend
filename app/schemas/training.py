from pydantic import BaseModel, ConfigDict, UUID4
from datetime import date, datetime, time
from typing import List, Optional

from app.enums.level import Level
from app.enums.style import Style


class TrainingBase(BaseModel):
    level: Level
    style: Style
    instructor_ids: List[UUID4]
    description: Optional[str] = None
    date: date
    time: time
    duration: int = 60
    price: int = 18
    currency: str = "USD"
    studio_id: UUID4
    flyer: Optional[str] = None
    max_slots: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class Training(TrainingBase):
    id: UUID4
    created_at: datetime


class CreateTraining(TrainingBase):
    pass
