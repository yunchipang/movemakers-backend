from pydantic import BaseModel, ConfigDict
from typing import Optional


# 3 schema classes, with the latter 2 inherits the first class BaseDancer
# to avoid duplication of model fields


# BaseDancer includes the most basic data that can be public facing
class BaseDancer(BaseModel):
    name: str
    instagram_handle: str
    youtube_channel: str
    bio: Optional[str] = None
    nationality: str
    based_in: str


class Dancer(BaseDancer):
    id: int

    model_config = ConfigDict(from_attributes=True)


class CreateDancer(BaseDancer):
    pass
