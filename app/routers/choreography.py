from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
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
    choreography = await choreography_services.get_choreography(
        choreo_id=choreo_id, db=db
    )
    if choreography is None:
        raise HTTPException(status_code=404, detail="Choreography does not exist")
    return choreography


@router.get("/{choreo_id}/repr", response_model=dict)
async def get_choreography_repr(choreo_id: str, db: Session = Depends(get_db)):
    choreography = await choreography_services.get_choreography(
        choreo_id=choreo_id, db=db
    )
    if choreography is None:
        raise HTTPException(status_code=404, detail="Choreography does not exist")
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
    if updated_choreography is None:
        raise HTTPException(status_code=404, detail="Choreography not found")
    return updated_choreography


@router.delete("/{choreo_id}")
async def delete_choreography(choreo_id: str, db: Session = Depends(get_db)):
    choreography = await choreography_services.get_choreography(
        choreo_id=choreo_id, db=db
    )
    if choreography is None:
        raise HTTPException(status_code=404, detail="Choreography does not exist")
    await choreography_services.delete_choreography(choreography, db=db)
    return "Successfully deleted the choreography"
