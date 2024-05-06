from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import studio as studio_exceptions
from app.schemas import studio as studio_schemas
from app.services import studio as studio_services

router = APIRouter()


# create a studio
@router.post("/", response_model=studio_schemas.Studio)
async def create_studio(
    studio: studio_schemas.CreateStudio,
    db: Session = Depends(get_db),
):
    return await studio_services.create_studio(studio=studio, db=db)


# get all studios
@router.get("/", response_model=List[studio_schemas.Studio])
async def get_studios(db: Session = Depends(get_db)):
    return await studio_services.get_all_studios(db=db)


# get studio by id
@router.get("/{studio_id}", response_model=studio_schemas.Studio)
async def get_studio(studio_id: str, db: Session = Depends(get_db)):
    try:
        studio = await studio_services.get_studio(studio_id=studio_id, db=db)
    except studio_exceptions.StudioNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return studio


@router.get("/{studio_id}/repr", response_model=dict)
async def get_studio_repr(studio_id: str, db: Session = Depends(get_db)):
    try:
        studio = await studio_services.get_studio(studio_id=studio_id, db=db)
    except studio_exceptions.StudioNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"__repr__": repr(studio)}


# update a studio by id
@router.put("/{studio_id}", response_model=studio_schemas.Studio)
async def update_studio(
    studio_id: str,
    studio_data: studio_schemas.UpdateStudio,
    db: Session = Depends(get_db),
):
    updated_studio = await studio_services.update_studio(
        studio_id=studio_id, studio_data=studio_data, db=db
    )
    return updated_studio


# delete a studio by id
@router.delete("/{studio_id}")
async def delete_studio(studio_id: str, db: Session = Depends(get_db)):
    try:
        studio = await studio_services.get_studio(studio_id=studio_id, db=db)
    except studio_exceptions.StudioNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    await studio_services.delete_studio(studio, db=db)
    return "Successfully deleted the studio"
