from typing import TYPE_CHECKING, List

from app.models import dancer as dancer_models
from app.models import studio as studio_models
from app.models import training as training_models
from app.schemas import training as training_schemas

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

import uuid


# create a training instance in database using the training data passed in
async def create_training(
    training: training_schemas.CreateTraining, db: "Session"
) -> training_schemas.Training:
    studio_id: uuid.UUID = training.studio_id
    instructor_ids: List[uuid.UUID] = training.instructor_ids
    training_data = training.model_dump(exclude={"studio", "instructor_ids"})

    new_training = training_models.Training(**training_data)
    db.add(new_training)
    db.flush()

    studio = (
        db.query(studio_models.Studio)
        .filter(studio_models.Studio.id == studio_id)
        .first()
    )
    new_training.studio = studio
    instructors = (
        db.query(dancer_models.Dancer)
        .filter(dancer_models.Dancer.id.in_(instructor_ids))
        .all()
    )
    new_training.instructors = instructors

    db.commit()
    db.refresh(new_training)
    return training_schemas.Training.model_validate(new_training)


# query database to get all trainings
async def get_all_trainings(db: "Session") -> List[training_schemas.Training]:
    trainings = db.query(training_models.Training).all()
    return [
        training_schemas.Training.model_validate(training) for training in trainings
    ]


# query database for a specific training with training id
async def get_training(training_id: str, db: "Session"):
    training = (
        db.query(training_models.Training)
        .filter(training_models.Training.id == training_id)
        .first()
    )
    return training


# delete a specific training from the database
async def delete_training(training: training_models.Training, db: "Session"):
    db.delete(training)
    db.commit()


# update a specific training
async def update_training(
    training_id: uuid.UUID,
    training_data: training_schemas.UpdateTraining,
    db: "Session",
) -> training_schemas.Training:
    training = (
        db.query(training_models.Training)
        .filter(training_models.Training.id == training_id)
        .first()
    )
    if not training:
        raise Exception("Training not found")

    for k, v in training_data.model_dump(exclude_unset=True).items():
        if k != "studio_id" and k != "instructor_ids" and hasattr(training, k):
            setattr(training, k, v)

    if training_data.studio_id is not None:
        new_studio = (
            db.query(studio_models.Studio)
            .fitler(studio_models.Studio.id == training_data.studio_id)
            .first()
        )
        training.studio = new_studio
    if training_data.instructor_ids is not None:
        new_instructors = (
            db.query(dancer_models.Dancer)
            .filter(dancer_models.Dancer.id.in_(training_data.instructor_ids))
            .all()
        )
        training.instructors = new_instructors

    db.commit()
    db.refresh(training)

    return training_schemas.Training.model_validate(training)
