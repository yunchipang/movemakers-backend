from pydantic import BaseModel
from models.person import Person
from models.studio import Studio


class Crew(BaseModel):
    name: str
    bio: str
    base: Studio
    directors: list[Person]
    members: list[Person]
    style: str
    formation_year: int
    instagram: str
    training_schedule: str
    performances: list[str]

    class Config:
        from_attributes = True