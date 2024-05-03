from datetime import datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel, ConfigDict

from app.enums.level import Level
from app.enums.style import Style
from app.schemas.dancer import Dancer
from app.schemas.studio import Studio


class BaseTraining(BaseModel):
    level: Level
    style: Style
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    price: int = 18
    currency: str = "USD"
    flyer: Optional[str] = None
    max_slots: int
    is_active: Optional[bool] = True

    model_config = ConfigDict(from_attributes=True)


class Training(BaseTraining):
    id: UUID4
    created_at: datetime
    studio: Studio
    instructors: List[Dancer]


class CreateTraining(BaseTraining):
    studio_id: UUID4
    instructor_ids: List[UUID4]


class UpdateTraining(BaseTraining):
    level: Optional[Level] = None
    style: Optional[Style] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    price: Optional[int] = None
    currency: Optional[str] = None
    flyer: Optional[str] = None
    max_slots: Optional[int] = None
    is_active: Optional[bool] = None
    studio_id: Optional[UUID4] = None
    instructor_ids: Optional[List[UUID4]] = []
