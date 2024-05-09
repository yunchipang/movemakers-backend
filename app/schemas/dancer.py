from datetime import date
from typing import Optional

from pydantic import UUID4, BaseModel, ConfigDict

from app.enums.pronouns import Pronouns

# 3 schema classes, with the latter 2 inherits the first class BaseDancer
# to avoid duplication of model fields


# BaseDancer includes the most basic data that can be public facing
class BaseDancer(BaseModel):
    name: str
    image_url: str = None
    pronouns: Optional[Pronouns] = None
    bio: Optional[str] = None
    date_of_birth: Optional[date] = None
    nationality: str
    based_in: str
    instagram: str
    youtube: Optional[str] = None
    agency: Optional[str] = None
    contact_email: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class Dancer(BaseDancer):
    id: UUID4


class CreateDancer(BaseDancer):
    pass


class UpdateDancer(BaseDancer):
    name: Optional[str] = None
    image_url: str = None
    pronouns: Optional[Pronouns] = None
    bio: Optional[str] = None
    date_of_birth: Optional[date] = None
    nationality: Optional[str] = None
    based_in: Optional[str] = None
    instagram: Optional[str] = None
    youtube: Optional[str] = None
    agency: Optional[str] = None
    contact_email: Optional[str] = None
