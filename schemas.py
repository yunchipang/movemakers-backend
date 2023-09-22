from typing import List, Optional
from pydantic import BaseModel


class BaseDancer(BaseModel):
    name: str
    instagram_handle: str
    roles: Optional[List[str]] = None
    styles: Optional[List[str]] = None

class Dancer(BaseDancer):
    id: int

class CreateDancer(BaseDancer):
    pass