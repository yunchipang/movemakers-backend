from typing import Optional

from pydantic import UUID4, BaseModel, ConfigDict


class BaseAgency(BaseModel):
    name: str
    website: Optional[str] = None
    instagram: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class Agency(BaseAgency):
    id: UUID4


class CreateAgency(BaseAgency):
    pass


class UpdateAgency(BaseAgency):
    name: Optional[str] = None
    website: Optional[str] = None
    instagram: Optional[str] = None
