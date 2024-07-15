from typing import Optional

from pydantic import UUID4, BaseModel, ConfigDict

from app.schemas.agency import Agency


class BaseContact(BaseModel):
    type: str
    name: Optional[str] = None
    email: str
    phone: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class Contact(BaseContact):
    id: UUID4
    agency: Optional[Agency] = None


class CreateContact(BaseContact):
    agency_id: Optional[UUID4] = None


class UpdateContact(BaseContact):
    type: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    agency_id: Optional[UUID4] = None
