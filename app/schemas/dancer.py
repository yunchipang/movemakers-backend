from pydantic import BaseModel, ConfigDict, UUID4
from typing import Optional
from datetime import date


# 3 schema classes, with the latter 2 inherits the first class BaseDancer
# to avoid duplication of model fields


# BaseDancer includes the most basic data that can be public facing
class BaseDancer(BaseModel):
    name: str
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
