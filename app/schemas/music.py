from typing import Optional

from pydantic import BaseModel, ConfigDict


class BaseMusic(BaseModel):
    spotify_track_id: str
    name: str
    artist: str

    model_config = ConfigDict(from_attributes=True)


class Music(BaseMusic):
    pass


class CreateMusic(BaseMusic):
    pass


class UpdateMusic(BaseMusic):
    spotify_track_id: Optional[str] = None
    name: Optional[str] = None
    artist: Optional[str] = None
