from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import user as user_models
from app.schemas import training as training_schemas
from app.services import training as training_services
from app.services import user as user_services

router = APIRouter()


# create a training
@router.post("/", response_model=training_schemas.Training)
async def create_training(
    training: training_schemas.CreateTraining,
    db: Session = Depends(get_db),
):
    return await training_services.create_training(training=training, db=db)


# get all trainings
@router.get("/", response_model=List[training_schemas.Training])
async def get_trainings(db: Session = Depends(get_db)):
    return await training_services.get_all_trainings(db=db)


# get a training by id
@router.get("/{training_id}", response_model=training_schemas.Training)
async def get_training(training_id: str, db: Session = Depends(get_db)):
    training = await training_services.get_training(training_id=training_id, db=db)
    if training is None:
        raise HTTPException(status_code=404, detail="Training does not exist")
    return training


# delete a training by id
@router.delete("/{training_id}")
async def delete_training(training_id: str, db: Session = Depends(get_db)):
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
    db: Session = Depends(get_db),
):
    updated_training = await training_services.update_training(
        training_id=training_id, training_data=training_data, db=db
    )
    if updated_training is None:
        raise HTTPException(status_code=404, detail="Training not found")
    return updated_training


# register a user for a training
@router.post("/{training_id}/register", status_code=status.HTTP_201_CREATED)
async def register_user_for_training(
    training_id: str,
    user: user_models.User = Depends(user_services.get_current_user),
    db: Session = Depends(get_db),
):
    success, message = await training_services.register_user_for_training(
        training_id=training_id, user_id=user.id, db=db
    )
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"message": message}


# cancel a user's registration for a training
@router.delete("/{training_id}/cancel")
async def cancel_registration_for_training(
    training_id: str,
    user: user_models.User = Depends(user_services.get_current_user),
    db: Session = Depends(get_db),
):
    success, message = await training_services.cancel_user_registration(
        training_id=training_id, user_id=user.id, db=db
    )
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"message": message}
