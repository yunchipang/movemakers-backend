from typing import Optional

from pydantic import UUID4, BaseModel, ConfigDict

from app.schemas.agency import Agency


class BaseContact(BaseModel):
    email: str
    agency: Optional[Agency]

    model_config = ConfigDict(from_attributes=True)


class Contact(BaseContact):
    id: UUID4


class CreateContact(BaseContact):
    pass


class UpdateContact(BaseContact):
    email: Optional[str]
    agency: Optional[Agency]
