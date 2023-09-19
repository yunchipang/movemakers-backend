from typing import Union
from fastapi import FastAPI, HTTPException
from bson import ObjectId

from models.choreo import Choreo
from models.person import Person
from models.studio import Studio
from models.crew import Crew

from pymongo import MongoClient
import settings

client = MongoClient(settings.mongodb_uri, settings.mongodb_port)
db = client["movemakers"]


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/studios/{studio_id}")
def read_studio(studio_id: int, q: Union[str, None] = None):
    return {"studio_id": studio_id, "q": q}

@app.put("/studios/{studio_id}")
def update_studio(studio_id: int, studio: Studio):
    return {"studio_name": studio.name, "studio_id": studio_id}

@app.get("/persons/{object_id}")
def read_person(object_id: str, q: Union[str, None] = None):
    collection = db['persons']
    person = collection.find_one({"_id": ObjectId(object_id)})
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    
    person['_id'] = str(person["_id"])
    return {"object_id": object_id, "q": q, "person": person}

@app.put("/persons/{person_id}")
def update_person(person_id: str, person: Person):
    return {"person_name": person.name, "person_id": person_id}

@app.get("/choreos/{choreo_id}")
def read_choreo(choreo_id: int, q: Union[str, None] = None):
    return {"choreo_id": choreo_id, "q": q}

@app.put("/choreos/{choreo_id}")
def update_choreo(choreo_id: int, choreo: Choreo):
    return {"choreo_name": choreo.name, "choreo_id": choreo_id}

@app.get("/crews/{crew_id}")
def read_crew(crew_id: int, q: Union[str, None] = None):
    return {"crew_id": crew_id, "q": q}

@app.put("/crews/{crew_id}")
def update_crew(crew_id: int, crew: Crew):
    return {"crew_name": crew.name, "crew_id": crew_id}