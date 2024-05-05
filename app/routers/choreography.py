from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import choreography as choreography_exceptions
from app.schemas import choreography as choreography_schemas
from app.services import choreography as choreography_services

router = APIRouter()


@router.post("/", response_model=choreography_schemas.Choreography)
async def create_choreography(
    choreography: choreography_schemas.CreateChoreography,
    db: Session = Depends(get_db),
):
    return await choreography_services.create_choreography(
        choreography=choreography, db=db
    )


@router.get("/", response_model=List[choreography_schemas.Choreography])
async def get_all_choreos(db: Session = Depends(get_db)):
    return await choreography_services.get_all_choreos(db=db)


@router.get("/{choreo_id}", response_model=choreography_schemas.Choreography)
async def get_choreography(choreo_id: str, db: Session = Depends(get_db)):
    try:
        choreography = await choreography_services.get_choreography(
            choreo_id=choreo_id, db=db
        )
    except choreography_exceptions.ChoreographyNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return choreography


@router.get("/{choreo_id}/repr", response_model=dict)
async def get_choreography_repr(choreo_id: str, db: Session = Depends(get_db)):
    try:
        choreography = await choreography_services.get_choreography(
            choreo_id=choreo_id, db=db
        )
    except choreography_exceptions.ChoreographyNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"__repr__": repr(choreography)}


@router.put("/{choreo_id}", response_model=choreography_schemas.Choreography)
async def update_choreography(
    choreo_id: str,
    choreo_data: choreography_schemas.UpdateChoreography,
    db: Session = Depends(get_db),
):
    updated_choreography = await choreography_services.update_choreography(
        choreo_id=choreo_id, choreo_data=choreo_data, db=db
    )
    return updated_choreography


@router.delete("/{choreo_id}")
async def delete_choreography(choreo_id: str, db: Session = Depends(get_db)):
    try:
        choreography = await choreography_services.get_choreography(
            choreo_id=choreo_id, db=db
        )
    except choreography_exceptions.ChoreographyNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    await choreography_services.delete_choreography(choreography, db=db)
    return "Successfully deleted the choreography"
