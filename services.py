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

async def create_dancer(dancer: schemas.CreateDancer, db: "Session") -> schemas.Dancer:
    # create a dancer instance in database using the dancer data passed in
    dancer = models.Dancer(**dancer.dict())
    db.add(dancer)
    db.commit()
    db.refresh(dancer)
    return schemas.Dancer.from_orm(dancer)

async def get_all_dancers(db: "Session") -> List[schemas.Dancer]:
    # query database to get all dancers
    dancers = db.query(models.Dancer).all()
    return list(map(schemas.Dancer.from_orm, dancers))