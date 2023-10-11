from typing import TYPE_CHECKING, List

from app import database, models, schemas

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def add_tables():
    # return database.Base.metadata.create_all(bind=database.engine)
    existing_table_names = database.engine.table_names()
    for table in database.Base.metadata.tables.values():
        if table.name not in existing_table_names:
            table.create(database.engine)

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

# update a specific dancer in the database
async def update_dancer(
        dancer_data: schemas.CreateDancer, dancer: models.Dancer, db: "Session"
) -> schemas.Dancer:
    # feed data one to one into the dancer object
    dancer.name = dancer_data.name
    dancer.instagram_handle = dancer_data.instagram_handle
    dancer.rols = dancer_data.roles
    dancer.styles = dancer_data.styles

    db.commit()
    db.refresh(dancer)

    return schemas.Dancer.from_orm(dancer)
