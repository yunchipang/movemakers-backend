from typing import TYPE_CHECKING, List

import database
import models
import schemas

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def add_tables():
    return database.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# create a dancer instance in database using the dancer data passed in
async def create_dancer(dancer: schemas.CreateDancer, db: "Session") -> schemas.Dancer:
    dancer = models.Dancer(**dancer.dict())
    db.add(dancer)
    db.commit()
    db.refresh(dancer)
    return schemas.Dancer.from_orm(dancer)

# query database to get all dancers
async def get_all_dancers(db: "Session") -> List[schemas.Dancer]:
    dancers = db.query(models.Dancer).all()
    return list(map(schemas.Dancer.from_orm, dancers))

# query database for a specific dancer with the dancer id
async def get_dancer(dancer_id: int, db: "Session"):
    dancer = db.query(models.Dancer).filter(models.Dancer.id == dancer_id).first()
    return dancer

# delete a specific dancer from the database
async def delete_dancer(dancer: models.Dancer, db: "Session"):
    db.delete(dancer)
    db.commit()