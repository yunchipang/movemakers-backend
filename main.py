from typing import Union
from fastapi import FastAPI, HTTPException, status
from bson import ObjectId
from bson.errors import InvalidId

from models.studio import Studio

from pymongo import MongoClient
import settings

client = MongoClient(settings.mongodb_uri, settings.mongodb_port)
db = client['movemakers']


app = FastAPI()


@app.get('/')
def read_root():
    return {'Hello': 'Welcome to MoveMakers API 🕺🏻'}

@app.get('/studios/{object_id}', status_code=status.HTTP_200_OK, response_model=Studio)
def read_studio(object_id: str, q: Union[str, None] = None):
    try:
        collection = db['studios']
        data = collection.find_one({'_id': ObjectId(object_id)})
        if data is None:
            raise HTTPException(status_code=404, detail='Studio not found')
        return {'object_id': object_id, 'q': q, 'data': data}
    except InvalidId:
        raise HTTPException(status_code=400, detail='Invalid object ID')
    except Exception:
        raise HTTPException(status_code=500, detail='Internal server error')

@app.get('/persons/{object_id}')
def read_person(object_id: str, q: Union[str, None] = None):
    try:
        collection = db['persons']
        person = collection.find_one({'_id': ObjectId(object_id)})
        if person is None:
            raise HTTPException(status_code=404, detail='Person not found')
        
        person['_id'] = str(person['_id'])
        return {'object_id': object_id, 'q': q, 'data': person}
    except InvalidId:
        raise HTTPException(status_code=400, detail='Invalid object ID')
    except Exception:
        raise HTTPException(status_code=500, detail='Internal server error')

@app.get('/choreos/{object_id}')
def read_choreo(object_id: str, q: Union[str, None] = None):
    try:
        collection = db['choreos']
        choreo = collection.find_one({'_id': ObjectId(object_id)})
        if choreo is None:
            raise HTTPException(status_code=404, detail='Choreo not found')
        
        
        choreo['_id'] = str(choreo['_id'])
        return {'object_id': object_id, 'q': q, 'data': choreo}
    except InvalidId:
        raise HTTPException(status_code=400, detail='Invalid object ID')
    except Exception:
        raise HTTPException(status_code=500, detail='Internal server error')

@app.get('/crews/{object_id}')
def read_crew(object_id: str, q: Union[str, None] = None):
    try:
        collection = db['crews']
        crew = collection.find_one({'_id': ObjectId(object_id)})
        if crew is None:
            raise HTTPException(status_code=404, detail='Crew not found')
        
        crew['_id'] = str(crew['_id'])
        return {'object_id': object_id, 'q': q, 'data': crew}
    except InvalidId:
        raise HTTPException(status_code=400, detail='Invalid object ID')
    except Exception:
        raise HTTPException(status_code=500, detail='Internal server error')

