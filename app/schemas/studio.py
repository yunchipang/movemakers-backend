from pydantic import BaseModel, UUID4
from typing import Optional
from app.models.dancer import Dancer


class BaseStudio(BaseModel):
    name: str
    address: str
    email: str
    phone: str
    opening_hours: str
    owners: Optional[Dancer] = None
    room_count: Optional[int] = None
    founded_in: Optional[int] = None
    instagram: str
    youtube: str
    website: str

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class Studio(BaseStudio):
    id: UUID4


class CreateStudio(BaseStudio):
    pass
