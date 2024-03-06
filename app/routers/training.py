from typing import List

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app import database
from app.schemas import training as training_schemas
from app.services import training as training_services


router = APIRouter()

# get all trainings
@router.get("/", response_model=List[training_schemas.Training])
async def get_dancers(db: Session=Depends(database.get_db)):
    return await training_services.get_all_trainings(db=db)
