from pydantic import BaseModel, ConfigDict
from typing import Optional


class BaseStudio(BaseModel):
    name: str
    instagram_handle: str
    youtube_channel: str
    address: str
    email: str
    phone: str
    opening_hours: str
    website: str
    owner: Optional[str] = None
    room_count: Optional[int] = None
    since: Optional[int] = None


class Studio(BaseStudio):
    id: int

    model_config = ConfigDict(from_attributes=True)


class CreateStudio(BaseStudio):
    pass
