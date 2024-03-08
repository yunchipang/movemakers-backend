from typing import List

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.database import database
from app.schemas import crew as crew_schemas
from app.services import crew as crew_services


router = APIRouter()


# create a crew
@router.post("/", response_model=crew_schemas.Crew)
async def create_crew(
    crew: crew_schemas.CreateCrew,
    db: Session = Depends(database.get_db),
):
    return await crew_services.create_crew(crew=crew, db=db)


# get all crews
@router.get("/", response_model=List[crew_schemas.Crew])
async def get_crews(db: Session = Depends(database.get_db)):
    return await crew_services.get_all_crews(db=db)


# get crew by id
@router.get("/{crew_id}", response_model=crew_schemas.Crew)
async def get_crew(crew_id: str, db: Session = Depends(database.get_db)):
    crew = await crew_services.get_crew(crew_id=crew_id, db=db)
    if crew is None:
        raise HTTPException(status_code=404, detail="Crew does not exist")
    return crew


# delete a crew by id
@router.delete("/{crew_id}")
async def delete_crew(crew_id: str, db: Session = Depends(database.get_db)):
    crew = await crew_services.get_crew(crew_id=crew_id, db=db)
    if crew is None:
        raise HTTPException(status_code=404, detail="Crew does not exist")

    await crew_services.delete_crew(crew, db=db)
    return "Successfully deleted the crew"


# update a crew by id
@router.put("/{crew_id}", response_model=crew_schemas.Crew)
async def update_crew(
    crew_id: str,
    crew_data: crew_schemas.CreateCrew,
    db: Session = Depends(database.get_db),
):
    crew = await crew_services.get_crew(crew_id=crew_id, db=db)
    if crew is None:
        raise HTTPException(status_code=404, detail="Crew does not exist")

    return await crew_services.update_crew(crew_data=crew_data, crew=crew, db=db)
