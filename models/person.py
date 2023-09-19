from pydantic import BaseModel
from enums.role import Role


class Person(BaseModel):
    name: str
    instagram: str
    role: list[Role]
    bio: str