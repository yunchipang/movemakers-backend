from typing import TYPE_CHECKING, List
import fastapi

from sqlalchemy import orm
from app import schemas
from app import services

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


app = fastapi.FastAPI()


@app.get("/api/")
async def get_root():
    return {"message": "Welcome to MoveMakers API🕺🏻"}

@app.post("/api/dancers/", response_model=schemas.Dancer)
async def create_dancer(
    dancer: schemas.CreateDancer, 
    db: orm.Session=fastapi.Depends(services.get_db),
):
    return await services.create_dancer(dancer=dancer, db=db)

@app.get("/api/dancers/", response_model=List[schemas.Dancer])
async def get_dancers(db: orm.Session=fastapi.Depends(services.get_db)):
    return await services.get_all_dancers(db=db)

@app.get("/api/dancers/{dancer_id}", response_model=schemas.Dancer)
async def get_dancer(
    dancer_id: int, 
    db: orm.Session=fastapi.Depends(services.get_db)
):
    dancer = await services.get_dancer(dancer_id=dancer_id, db=db)
    print("dancer=", dancer)
    if dancer is None:
        raise fastapi.HTTPException(status_code=404, detail="Dancer does not exist")
    
    return dancer

@app.delete("/api/dancers/{dancer_id}")
async def delete_dancer(
    dancer_id: int,
    db: orm.Session=fastapi.Depends(services.get_db)
):
    dancer = await services.get_dancer(dancer_id=dancer_id, db=db)
    if dancer is None:
        raise fastapi.HTTPException(status_code=404, detail="Dancer does not exist")

    await services.delete_dancer(dancer, db=db)
    return "successfully deleted the dancer"

@app.put("/api/dancers/{dancer_id}", response_model=schemas.Dancer)
async def update_dancer(
    dancer_id: int,
    dancer_data: schemas.CreateDancer,
    db: orm.Session=fastapi.Depends(services.get_db)
):
    dancer = await services.get_dancer(dancer_id=dancer_id, db=db)
    if dancer is None:
        raise fastapi.HTTPException(status_code=404, detail="Dancer does not exist")

    return await services.update_dancer(dancer_data=dancer_data, dancer=dancer, db=db)