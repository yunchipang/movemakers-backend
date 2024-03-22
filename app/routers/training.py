from typing import List

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app import database
from app.schemas import training as training_schemas
from app.services import training as training_services


router = APIRouter()


# create a training
@router.post("/", response_model=training_schemas.Training)
async def create_training(
    training: training_schemas.CreateTraining,
    db: Session = Depends(database.get_db),
):
    return await training_services.create_training(training=training, db=db)


# get all trainings
@router.get("/", response_model=List[training_schemas.Training])
async def get_trainings(db: Session = Depends(database.get_db)):
    return await training_services.get_all_trainings(db=db)


# get a training by id
@router.get("/{training_id}", response_model=training_schemas.Training)
async def get_training(training_id: str, db: Session = Depends(database.get_db)):
    training = await training_services.get_training(training_id=training_id, db=db)
    if training is None:
        raise HTTPException(status_code=404, detail="Training does not exist")
    return training


# delete a training by id
@router.delete("/{training_id}")
async def delete_training(training_id: str, db: Session = Depends(database.get_db)):
    training = await training_services.get_training(training_id=training_id, db=db)
    if training is None:
        raise HTTPException(status_code=404, detail="Training does not exist")
    await training_services.delete_training(training, db=db)
    return "Successfully deleted the training"


# update a training by id
@router.put("/{training_id}", response_model=training_schemas.Training)
async def update_training(
    training_id: str,
    training_data: training_schemas.UpdateTraining,
    db: Session = Depends(database.get_db),
):
    updated_training = await training_services.update_studio(
        studio_id=training_id, studio_data=training_data, db=db
    )
    if updated_training is None:
        raise HTTPException(status_code=404, detail="Training not found")
    return updated_training
