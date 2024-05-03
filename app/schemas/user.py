from pydantic import UUID4, BaseModel, ConfigDict, EmailStr, Field


# user
class BaseUser(BaseModel):
    email: EmailStr
    username: str
    first_name: str | None = None
    last_name: str | None = None
    disabled: bool | None = False

    model_config = ConfigDict(from_attributes=True)


class User(BaseUser):
    id: UUID4


class CreateUser(BaseUser):
    hashed_password: bytes = Field(alias="password")
