from typing import List, Optional

from pydantic import UUID4, BaseModel, ConfigDict

from app.schemas.dancer import Dancer


class BaseStudio(BaseModel):
    name: str
    address: str
    email: str
    phone: str
    opening_hours: str
    room_count: Optional[int] = None
    founded_in: Optional[int] = None
    instagram: str
    youtube: str
    website: str

    model_config = ConfigDict(from_attributes=True)


# serves as the response model for endpoints querying studio details
class Studio(BaseStudio):
    id: UUID4
    owners: List[Dancer] = []


class CreateStudio(BaseStudio):
    owner_ids: Optional[List[UUID4]] = []


class UpdateStudio(BaseStudio):
    name: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    opening_hours: Optional[str] = None
    room_count: Optional[int] = None
    founded_in: Optional[int] = None
    instagram: Optional[str] = None
    youtube: Optional[str] = None
    website: Optional[str] = None
    owner_ids: Optional[List[UUID4]] = []
