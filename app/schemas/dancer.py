from typing import List, Optional
from pydantic import BaseModel, ConfigDict


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