from datetime import datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel, ConfigDict

from app.enums.level import Level
from app.enums.style import Style
from app.schemas.dancer import Dancer
from app.schemas.music import Music


class BaseChoreography(BaseModel):
    description: Optional[str] = None
    level: Level
    styles: List[Style]
    videos: List[str]

    model_config = ConfigDict(from_attributes=True)


class Choreography(BaseChoreography):
    id: UUID4
    created_at: datetime
    music: Music
    choreographers: List[Dancer]


class CreateChoreography(BaseChoreography):
    music_id: str
    choreographer_ids: List[UUID4]


class UpdateChoreography(BaseChoreography):
    description: Optional[str] = None
    level: Optional[Level] = None
    styles: Optional[List[Style]] = []
    videos: Optional[List[str]] = None
    music_id: Optional[str] = None
    choreographer_ids: Optional[List[UUID4]] = []
