from pydantic import BaseModel, ConfigDict, HttpUrl, UUID4
from typing import List, Optional

from ..models.training import StyleEnum


class BaseCrew(BaseModel):
    name: str
    bio: Optional[str] = None
    based_in: str
    styles: List[StyleEnum]
    directors: List[UUID4]
    captains: Optional[List[UUID4]]
    members: Optional[List[UUID4]]
    rehearsal_schedules: Optional[str] = None
    instagram: str
    youtube: Optional[str] = None
    website: Optional[HttpUrl] = None


class Crew(BaseCrew):
    id: UUID4

    model_config = ConfigDict(from_attributes=True)


class CreateCrew(BaseCrew):
    pass
