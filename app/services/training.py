from typing import TYPE_CHECKING

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
