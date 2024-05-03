from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import dancer as dancer_schemas
from app.services import dancer as dancer_services

router = APIRouter()


# create a dancer
@router.post("/", response_model=dancer_schemas.Dancer)
async def create_dancer(
    dancer: dancer_schemas.CreateDancer,
    db: Session = Depends(get_db),
):
    return await dancer_services.create_dancer(dancer=dancer, db=db)


# get all dancers
@router.get("/", response_model=List[dancer_schemas.Dancer])
async def get_dancers(db: Session = Depends(get_db)):
    return await dancer_services.get_all_dancers(db=db)


# get dancer by id
@router.get("/{dancer_id}", response_model=dancer_schemas.Dancer)
async def get_dancer(dancer_id: str, db: Session = Depends(get_db)):
    dancer = await dancer_services.get_dancer(dancer_id=dancer_id, db=db)
    if dancer is None:
        raise HTTPException(status_code=404, detail="Dancer does not exist")
    return dancer


# update a dancer by id
@router.put("/{dancer_id}", response_model=dancer_schemas.Dancer)
async def update_dancer(
    dancer_id: str,
    dancer_data: dancer_schemas.UpdateDancer,
    db: Session = Depends(get_db),
):
    updated_dancer = await dancer_services.update_dancer(
        dancer_id=dancer_id, dancer_data=dancer_data, db=db
    )
    if updated_dancer is None:
        raise HTTPException(status_code=404, detail="Dancer not found")
    return updated_dancer


# delete a dancer by id
@router.delete("/{dancer_id}")
async def delete_dancer(dancer_id: str, db: Session = Depends(get_db)):
    dancer = await dancer_services.get_dancer(dancer_id=dancer_id, db=db)
    if dancer is None:
        raise HTTPException(status_code=404, detail="Dancer does not exist")

    await dancer_services.delete_dancer(dancer, db=db)
    return "Successfully deleted the dancer"
