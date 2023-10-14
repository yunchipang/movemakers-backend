from typing import TYPE_CHECKING, List
from fastapi import FastAPI, Depends, HTTPException

from sqlalchemy import orm

from app import database
from app.schemas import dancer as dancer_schemas
from app.services import dancer as dancer_services

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    # create tables if they do not exist yet
    database.add_tables()

@app.get("/")
async def get_root():
    return {"message": "Welcome to MoveMakers API"}

@app.post("/dancers/", response_model=dancer_schemas.Dancer)
async def create_dancer(
    dancer: dancer_schemas.CreateDancer, 
    db: orm.Session=Depends(database.get_db),
):
    return await dancer_services.create_dancer(dancer=dancer, db=db)

@app.get("/dancers/", response_model=List[dancer_schemas.Dancer])
async def get_dancers(db: orm.Session=Depends(database.get_db)):
    return await dancer_services.get_all_dancers(db=db)

@app.get("/dancers/{dancer_id}", response_model=dancer_schemas.Dancer)
async def get_dancer(
    dancer_id: int, 
    db: orm.Session=Depends(database.get_db)
):
    dancer = await dancer_services.get_dancer(dancer_id=dancer_id, db=db)
    print("dancer=", dancer)
    if dancer is None:
        raise HTTPException(status_code=404, detail="Dancer does not exist")
    
    return dancer

@app.delete("/dancers/{dancer_id}")
async def delete_dancer(
    dancer_id: int,
    db: orm.Session=Depends(database.get_db)
):
    dancer = await dancer_services.get_dancer(dancer_id=dancer_id, db=db)
    if dancer is None:
        raise HTTPException(status_code=404, detail="Dancer does not exist")

    await dancer_services.delete_dancer(dancer, db=db)
    return "successfully deleted the dancer"

@app.put("/dancers/{dancer_id}", response_model=dancer_schemas.Dancer)
async def update_dancer(
    dancer_id: int,
    dancer_data: dancer_schemas.CreateDancer,
    db: orm.Session=Depends(database.get_db)
):
    dancer = await dancer_services.get_dancer(dancer_id=dancer_id, db=db)
    if dancer is None:
        raise HTTPException(status_code=404, detail="Dancer does not exist")

    return await dancer_services.update_dancer(dancer_data=dancer_data, dancer=dancer, db=db)
