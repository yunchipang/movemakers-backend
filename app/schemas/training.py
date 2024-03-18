from pydantic import BaseModel, ConfigDict, UUID4
from datetime import date, datetime, time
from typing import List, Optional

from app.enums.level import Level
from app.enums.style import Style
from app.models.dancer import Dancer
from app.models.studio import Studio


class BaseTraining(BaseModel):
    level: Level
    style: Style
    description: Optional[str] = None
    date: date
    time: time
    duration: int = 60
    price: int = 18
    currency: str = "USD"
    flyer: Optional[str] = None
    capacity: int
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class Training(BaseTraining):
    id: UUID4
    created_at: datetime
    instructors: List[Dancer]
    studio: Studio


class CreateTraining(BaseTraining):
    pass
