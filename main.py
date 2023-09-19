from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

app = FastAPI()


class Style(Enum):
    hip_hop = "Hip Hop"
    contemporary = "Contemporary"
    jazz = "Jazz"
    afro = "Afro"
    dancehall = "Dancehall"
    heels = "heels"
    reggaeton = "Reggaetón"

class Level(Enum):
    beginner = "Beginner"
    intermediate = "Intermediate"
    advanced = "Advanced"
    all_levels = "All Levels"

class Role(Enum):
    instructor = "instructor"
    choreographer = "choreographer"
    director = "director"

class Studio(BaseModel):
    name: str
    city: str
    state: str
    address: str
    opening_hours: str
    phone_number: str
    email: str
    website: str
    instagram: str
    dance_styles: list[str]
    instructors: list[str]

class Person(BaseModel):
    name: str
    instagram: str
    role: list[str]
    crew: list[Crew]
    teach_at: list[Studio]
    bio: str

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

class Choreo(BaseModel):
    created_at: datetime
    choreographer: Person
    music: str
    style: Style
    level: Level
    video: str


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/studios/{studio_id}")
def read_studio(studio_id: int, q: Union[str, None] = None):
    return {"studio_id": studio_id, "q": q}

@app.put("/studios/{studio_id}")
def update_studio(studio_id: int, studio: Studio):
    return {"studio_name": studio.name, "studio_id": studio_id}

@app.get("/persons/{person_id}")
def read_person(person_id: int, q: Union[str, None] = None):
    return {"person_id": person_id, "q": q}

@app.put("/persons/{person_id}")
def update_person(person_id: int, person: Person):
    return {"person_name": person.name, "person_id": person_id}

@app.get("/choreos/{choreo_id}")
def read_choreo(choreo_id: int, q: Union[str, None] = None):
    return {"choreo_id": choreo_id, "q": q}

@app.put("/choreos/{choreo_id}")
def update_choreo(choreo_id: int, choreo: Choreo):
    return {"choreo_name": choreo.name, "choreo_id": choreo_id}