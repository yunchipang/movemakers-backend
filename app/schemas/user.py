import uuid
from pydantic import BaseModel, Field, EmailStr, ConfigDict, UUID4


class BaseUser(BaseModel):
    email: EmailStr

class User(BaseUser):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    is_active: bool = Field(default=False)
    model_config = ConfigDict(from_attributes=True)

class CreateUser(BaseUser):
    hashed_password: str = Field(alias="password")