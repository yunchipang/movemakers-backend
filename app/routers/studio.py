from typing import List

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app import database
from app.schemas import studio as studio_schemas
from app.services import studio as studio_services


router = APIRouter()


# create a studio
@router.post("/", response_model=studio_schemas.Studio)
async def create_studio(
    studio: studio_schemas.CreateStudio,
    db: Session = Depends(database.get_db),
):
    return await studio_services.create_studio(studio=studio, db=db)


# get all studios
@router.get("/", response_model=List[studio_schemas.Studio])
async def get_studios(db: Session = Depends(database.get_db)):
    return await studio_services.get_all_studios(db=db)


# get studio by id
@router.get("/{studio_id}", response_model=studio_schemas.Studio)
async def get_studio(studio_id: str, db: Session = Depends(database.get_db)):
    studio = await studio_services.get_studio(studio_id=studio_id, db=db)
    if studio is None:
        raise HTTPException(status_code=404, detail="Studio does not exist")
    return studio


# delete a studio by id
@router.delete("/{studio_id}")
async def delete_studio(studio_id: str, db: Session = Depends(database.get_db)):
    studio = await studio_services.get_studio(studio_id=studio_id, db=db)
    if studio is None:
        raise HTTPException(status_code=404, detail="Studio does not exist")

    await studio_services.delete_studio(studio, db=db)
    return "Successfully deleted the studio"


# update a studio by id
@router.put("/{studio_id}", response_model=studio_schemas.Studio)
async def update_studio(
    studio_id: str,
    studio_data: studio_schemas.CreateStudio,
    db: Session = Depends(database.get_db),
):
    studio = await studio_services.get_studio(studio_id=studio_id, db=db)
    if studio is None:
        raise HTTPException(status_code=404, detail="Studio does not exist")

    return await studio_services.update_studio(
        studio_data=studio_data, studio=studio, db=db
    )
