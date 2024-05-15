from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import agency as agency_exceptions
from app.schemas import agency as agency_schemas
from app.services import agency as agency_services

router = APIRouter()


@router.post("/", response_model=agency_schemas.Agency)
async def create_agency(
    agency: agency_schemas.CreateAgency,
    db: Session = Depends(get_db),
):
    try:
        new_agency = await agency_services.create_agency(agency=agency, db=db)
    except agency_exceptions.AgencyDuplicateError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        # general exception handling, consider logging the error
        raise HTTPException(status_code=500, detail=str(e))
    return new_agency


@router.get("/", response_model=List[agency_schemas.Agency])
async def get_all_agencies(db: Session = Depends(get_db)):
    return await agency_services.get_all_agencies(db=db)
