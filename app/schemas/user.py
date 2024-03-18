from pydantic import BaseModel, Field, EmailStr, UUID4


# user
class BaseUser(BaseModel):
    email: EmailStr

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class User(BaseUser):
    id: UUID4


class CreateUser(BaseUser):
    hashed_password: str = Field(alias="password")


# user login
class UserLogin(BaseModel):
    email: EmailStr
    password: str
