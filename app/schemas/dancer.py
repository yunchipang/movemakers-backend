from datetime import date
from typing import Optional, List

from pydantic import UUID4, BaseModel, ConfigDict, Field

from app.enums.pronouns import Pronouns
from app.schemas.contact import Contact

# 3 schema classes, with the latter 2 inherits the first class BaseDancer
# to avoid duplication of model fields


# BaseDancer includes the most basic data that can be public facing
class BaseDancer(BaseModel):
    name: str
    name_orig: str
    image_url: str = None
    pronouns: Optional[Pronouns] = None
    bio: Optional[str] = None
    date_of_birth: Optional[date] = None
    nationality: str
    based_in: str
    instagram: str
    youtube: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class Dancer(BaseDancer):
    id: UUID4
    contacts: List[Contact]

class CreateDancer(BaseDancer):
    contact_ids: List[UUID4] = Field(default_factory=list)


class UpdateDancer(BaseDancer):
    name: Optional[str] = None
    name_orig: Optional[str] = None
    image_url: Optional[str] = None
    pronouns: Optional[Pronouns] = None
    bio: Optional[str] = None
    date_of_birth: Optional[date] = None
    nationality: Optional[str] = None
    based_in: Optional[str] = None
    instagram: Optional[str] = None
    youtube: Optional[str] = None
    contact_ids: Optional[List[UUID4]] = Field(default_factory=list)
