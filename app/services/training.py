import uuid
from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from app.association import training_registration_association
from app.database import get_db
from app.exceptions import training as training_exceptions
from app.exceptions import user as user_exceptions
from app.models import training as training_models
from app.schemas import training as training_schemas
from app.services import dancer as dancer_services
from app.services import studio as studio_services
from app.services import user as user_services


# create a training instance in database using the training data passed in
async def create_training(
    training: training_schemas.CreateTraining, db: Session = Depends(get_db)
) -> training_schemas.Training:
    training_data = training.model_dump(exclude={"studio", "instructor_ids"})

    new_training = training_models.Training(**training_data)
    db.add(new_training)
    db.flush()

    studio = await studio_services.get_studio(training.studio_id, db=db)
    new_training.studio = studio
    instructors = await dancer_services.get_dancers(training.instructor_ids, db=db)
    new_training.instructors = instructors

    db.commit()
    db.refresh(new_training)

    return training_schemas.Training.model_validate(new_training)


# query database to get all trainings
async def get_all_trainings(
    db: Session = Depends(get_db),
) -> List[training_schemas.Training]:
    trainings = db.query(training_models.Training).all()
    return [
        training_schemas.Training.model_validate(training) for training in trainings
    ]


# query database for a specific training with training id
async def get_training(training_id: str, db: Session = Depends(get_db)):
    training = (
        db.query(training_models.Training)
        .filter(training_models.Training.id == training_id)
        .first()
    )
    if not training:
        raise training_exceptions.TrainingNotFoundError
    return training


# update a specific training
async def update_training(
    training_id: uuid.UUID,
    training_data: training_schemas.UpdateTraining,
    db: Session = Depends(get_db),
) -> training_schemas.Training:

    training = await get_training(training_id=training_id, db=db)
    for k, v in training_data.model_dump(exclude_unset=True).items():
        if k != "studio_id" and k != "instructor_ids" and hasattr(training, k):
            setattr(training, k, v)

    if training_data.studio_id:
        new_studio = await studio_services.get_studio(training_data.studio_id, db=db)
        training.studio = new_studio
    if training_data.instructor_ids:
        new_instructors = await dancer_services.get_dancers(
            training_data.instructor_ids, db=db
        )
        training.instructors = new_instructors

    db.commit()
    db.refresh(training)

    return training_schemas.Training.model_validate(training)


# delete a specific training from the database
async def delete_training(
    training: training_models.Training, db: Session = Depends(get_db)
):
    db.delete(training)
    db.commit()


async def register_user_for_training(
    training_id: str, user_id: str, db: Session = Depends(get_db)
) -> str:

    try:
        # get training and user
        training = await get_training(training_id=training_id, db=db)
        user = await user_services.get_user_by_id(user_id, db=db)

        # register user to the training
        # check if the training is full
        if len(training.participants) >= training.max_slots:
            raise training_exceptions.TrainingFullError
        # check if the user is already registered
        is_registered = (
            db.query(training_registration_association)
            .filter_by(training_id=training_id, user_id=user_id)
            .first()
        )
        if is_registered:
            raise user_exceptions.UserAlreadyRegisteredError

        training.participants.append(user)
        db.commit()

    except training_exceptions.TrainingNotFoundError as e:
        raise e
    except user_exceptions.UserNotFoundError as e:
        raise e

    return "User successfully registered for the training"


async def cancel_user_registration(
    training_id: str, user_id: str, db: Session = Depends(get_db)
) -> tuple[bool, str]:

    # check if training and user both exist
    training = await get_training(training_id, db=db)
    user = await user_services.get_user_by_id(user_id, db=db)

    # check if user is indeed currently registered to the training
    is_registered = (
        db.query(training_registration_association)
        .filter_by(training_id=training_id, user_id=user_id)
        .first()
    )
    if not is_registered:
        return False, "User is not registered for this training"

    # unregister the user from the training
    try:
        training.participants.remove(user)
        db.commit()
        return True, "User successfully unregistered from the training"
    except Exception as e:
        db.rollback()
        return False, f"Failed to unregister user: {e}"
