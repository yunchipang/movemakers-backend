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
    styles: List[Style]
    instagram: str
    youtube: Optional[str] = None
    website: Optional[HttpUrl] = None
    is_active: Optional[bool] = True

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class Crew(BaseCrew):
    id: UUID4
    home_studio: Optional[Studio] = None
    leaders: List[Dancer]
    members: List[Dancer]


class CreateCrew(BaseCrew):
    home_studio_id: Optional[UUID4] = None
    leader_ids: List[UUID4]
    member_ids: List[UUID4]


class UpdateCrew(BaseCrew):
    name: Optional[str] = None
    bio: Optional[str] = None
    based_in: Optional[str] = None
    founded_in: Optional[int] = None
    styles: Optional[List[Style]] = []
    instagram: Optional[str] = None
    youtube: Optional[str] = None
    website: Optional[HttpUrl] = None
    is_active: Optional[bool] = None
    home_studio_id: Optional[UUID4] = None
    leader_ids: Optional[List[UUID4]] = []
    member_ids: Optional[List[UUID4]] = []
