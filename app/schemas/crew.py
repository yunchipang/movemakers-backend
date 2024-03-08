from pydantic import BaseModel, ConfigDict, HttpUrl, UUID4
from typing import List, Optional

from app.models.training import StyleEnum


class BaseCrew(BaseModel):
    name: str
    bio: Optional[str] = None
    based_in: str
    founded_in: int
    home_studio: Optional[UUID4] = None
    styles: List[StyleEnum]
    director_ids: List[UUID4]
    captain_ids: Optional[List[UUID4]] = None
    member_ids: Optional[List[UUID4]] = None
    rehearsal_schedules: Optional[str] = None
    instagram: str
    youtube: Optional[str] = None
    website: Optional[HttpUrl] = None


class Crew(BaseCrew):
    id: UUID4

    model_config = ConfigDict(from_attributes=True)


class CreateCrew(BaseCrew):
    pass
