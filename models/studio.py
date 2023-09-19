from pydantic import BaseModel
from models.person import Person


class Studio(BaseModel):
    name: str
    city: str
    state: str
    address: str
    owner: list[Person]
    opening_hours: str
    phone_number: str
    email: str
    website: str
    instagram: str
    dance_styles: list[str]
    instructors: list[str]