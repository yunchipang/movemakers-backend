from pydantic import BaseModel, ConfigDict, HttpUrl, UUID4
from typing import List, Optional

from app.enums.style import Style
from app.models.dancer import Dancer
from app.models.studio import Studio


class BaseCrew(BaseModel):
    name: str
    bio: Optional[str] = None
    based_in: str
    founded_in: int
    home_studio: Optional[Studio] = None
    leader: Dancer
    members: List[Dancer]
    styles: List[Style]
    rehearsal_schedules: Optional[str] = None
    instagram: str
    youtube: Optional[str] = None
    website: Optional[HttpUrl] = None
    is_active: bool

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class Crew(BaseCrew):
    id: UUID4


class CreateCrew(BaseCrew):
    pass
