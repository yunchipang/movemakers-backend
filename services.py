from typing import TYPE_CHECKING

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
    dancer = models.Dancer(**dancer.dict())
    db.add(dancer)
    db.commit()
    db.refresh(dancer)
    return schemas.Dancer.from_orm(dancer)
