from pydantic import BaseModel, EmailStr
from enums.role import Role


class Person(BaseModel):
    name: str
    instagram: str
    email: EmailStr
    role: list[Role]
    bio: str

    class Config:
        from_attributes = True