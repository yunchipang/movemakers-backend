from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import training as training_exceptions
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
    try:
        training = await training_services.get_training(training_id, db=db)
    except training_exceptions.TrainingNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    return training


# get a training repr by id
@router.get("/{training_id}/repr", response_model=dict)
async def get_training_repr(training_id: str, db: Session = Depends(get_db)):
    try:
        training = await training_services.get_training(training_id, db=db)
    except training_exceptions.TrainingNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    return {"__repr__": repr(training)}


# update a training by id
@router.put("/{training_id}", response_model=training_schemas.Training)
async def update_training(
    training_id: str,
    training_data: training_schemas.UpdateTraining,
    db: Session = Depends(get_db),
):
    try:
        updated_training = await training_services.update_training(
            training_id=training_id, training_data=training_data, db=db
        )
    except training_exceptions.TrainingNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    return updated_training


# delete a training by id
@router.delete("/{training_id}")
async def delete_training(training_id: str, db: Session = Depends(get_db)):
    try:
        training = await training_services.get_training(training_id=training_id, db=db)
    except training_exceptions.TrainingNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    await training_services.delete_training(training, db=db)
    return "Successfully deleted the training"


# register a user for a training
@router.post("/{training_id}/register", status_code=status.HTTP_201_CREATED)
async def register_user_for_training(
    training_id: str,
    user: user_models.User = Depends(user_services.get_current_user),
    db: Session = Depends(get_db),
):
    try:
        res = await training_services.register_user_for_training(
            training_id=training_id, user_id=user.id, db=db
        )
    except Exception as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    return {"message": res}


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
