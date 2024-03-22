from pydantic import BaseModel, ConfigDict, UUID4
from typing import List, Optional


class BaseStudio(BaseModel):
    name: str
    address: str
    email: str
    phone: str
    opening_hours: str
    owner_ids: Optional[List[UUID4]] = None
    room_count: Optional[int] = None
    founded_in: Optional[int] = None
    instagram: str
    youtube: str
    website: str

    model_config = ConfigDict(from_attributes=True)


class Studio(BaseStudio):
    id: UUID4


class CreateStudio(BaseStudio):
    pass
