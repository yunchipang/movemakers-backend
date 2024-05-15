from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import crew as crew_exceptions
from app.schemas import crew as crew_schemas
from app.services import crew as crew_services

router = APIRouter()


# create a crew
@router.post("/", response_model=crew_schemas.Crew)
async def create_crew(
    crew: crew_schemas.CreateCrew,
    db: Session = Depends(get_db),
):
    return await crew_services.create_crew(crew=crew, db=db)


# get crews
@router.get("/", response_model=List[crew_schemas.Crew])
async def get_crews(dancer_id: Optional[str] = None, db: Session = Depends(get_db)):
    if dancer_id:
        return await crew_services.get_crews_by_dancer(dancer_id, db)
    else:
        return await crew_services.get_all_crews(db=db)


# get crew by id
@router.get("/{crew_id}", response_model=crew_schemas.Crew)
async def get_crew(crew_id: str, db: Session = Depends(get_db)):
    try:
        crew = await crew_services.get_crew(crew_id=crew_id, db=db)
    except crew_exceptions.CrewNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    return crew


@router.get("/{crew_id}/repr", response_model=dict)
async def get_crew_repr(crew_id: str, db: Session = Depends(get_db)):
    try:
        crew = await crew_services.get_crew(crew_id=crew_id, db=db)
    except crew_exceptions.CrewNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    return {"__repr__": repr(crew)}


# update a crew by id
@router.put("/{crew_id}", response_model=crew_schemas.Crew)
async def update_crew(
    crew_id: str,
    crew_data: crew_schemas.UpdateCrew,
    db: Session = Depends(get_db),
):
    updated_crew = await crew_services.update_crew(
        crew_id=crew_id, crew_data=crew_data, db=db
    )
    return updated_crew


# delete a crew by id
@router.delete("/{crew_id}")
async def delete_crew(crew_id: str, db: Session = Depends(get_db)):
    try:
        crew = await crew_services.get_crew(crew_id=crew_id, db=db)
    except crew_exceptions.CrewNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    await crew_services.delete_crew(crew, db=db)
    return "Successfully deleted the crew"
