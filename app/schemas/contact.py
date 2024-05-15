from typing import Optional

from pydantic import UUID4, BaseModel, ConfigDict

from app.schemas.agency import Agency


class BaseContact(BaseModel):
    email: str
    
    model_config = ConfigDict(from_attributes=True)


class Contact(BaseContact):
    id: UUID4
    agency: Optional[Agency] = None

class CreateContact(BaseContact):
    agency_id: Optional[UUID4] = None


class UpdateContact(BaseContact):
    email: Optional[str]
    agency_id: Optional[UUID4] = None
