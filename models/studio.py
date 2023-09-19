from pydantic import BaseModel, EmailStr, HttpUrl
from models.person import Person
from enums.style import Style


class Studio(BaseModel):
    name: str
    address: str
    owner: list[Person]
    opening_hours: str
    phone_number: str
    email: EmailStr
    website: HttpUrl
    instagram: str
    styles: list[Style]
    instructors: list[Person]