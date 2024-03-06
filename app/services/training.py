from typing import TYPE_CHECKING, List

from app.models import training as training_models
from app.schemas import training as training_schemas

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


# create a training instance in database using the training data passed in
async def create_training(training: training_schemas.CreateTraining, db: "Session") -> training_schemas.Training:
    training = training_models.Training(**training.dict())
    db.add(training)
    db.commit()
    db.refresh(training)
    return training_schemas.Training.from_orm(training)

# query database to get all trainings
async def get_all_trainings(db: "Session") -> List[training_schemas.Training]:
    trainings = db.query(training_models.Training).all()
    return list(map(training_schemas.Training.from_orm, trainings))

# query database for a specific training with training id
async def get_training(training_id: int, db: "Session"):
    training = db.query(training_models.Training).filter(training_models.Training.id == training_id).first()
    return training

# delete a specific training from the database
async def delete_training(training: training_models.Training, db: "Session"):
    db.delete(training)
    db.commit()

# update a specific training
async def update_training(
        training_data: training_schemas.CreateTraining, training: training_models.Training, db: "Session"
) -> training_schemas.Training:
    # feed data one to one into the training object
    training.level = training_data.level
    training.style = training_data.style
    training.instructor = training_data.instructor
    training.description = training_data.description
    training.date = training_data.date
    training.time = training_data.time
    training.duration = training_data.duration
    training.price = training_data.price
    training.currency = training_data.currency
    training.studio = training_data.studio
    training.flyer = training_data.flyer
    training.max_slots = training_data.max_slots
    training.is_active = training_data.is_active
