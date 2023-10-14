from typing import List, Optional
from pydantic import BaseModel, ConfigDict


# 3 schema classes, with the latter 2 inherits the first class BaseDancer
# to avoid duplication of model fields

# BaseDancer includes the most basic data that can be public facing
class BaseDancer(BaseModel):
    name: str
    instagram_handle: str
    roles: Optional[List[str]] = None
    styles: Optional[List[str]] = None

class Dancer(BaseDancer):
    id: int
    model_config = ConfigDict(from_attributes=True)

class CreateDancer(BaseDancer):
    pass