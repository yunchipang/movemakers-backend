from typing import TYPE_CHECKING, List

from app.models import dancer as dancer_models
from app.schemas import dancer as dancer_schemas

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


# create a dancer instance in database using the dancer data passed in
async def create_dancer(
    dancer: dancer_schemas.CreateDancer, db: "Session"
) -> dancer_schemas.Dancer:
    dancer = dancer_models.Dancer(**dancer.model_dump())
    db.add(dancer)
    db.commit()
    db.refresh(dancer)
    return dancer_schemas.Dancer.model_validate(dancer)


# query database to get all dancers
async def get_all_dancers(db: "Session") -> List[dancer_schemas.Dancer]:
    dancers = db.query(dancer_models.Dancer).all()
    return [dancer_schemas.Dancer.model_validate(dancer) for dancer in dancers]


# query database for a specific dancer with the dancer id
async def get_dancer(dancer_id: str, db: "Session"):
    dancer = (
        db.query(dancer_models.Dancer)
        .filter(dancer_models.Dancer.id == dancer_id)
        .first()
    )
    return dancer


# update a specific dancer in the database
async def update_dancer(
    dancer_data: dancer_schemas.CreateDancer,
    dancer: dancer_models.Dancer,
    db: "Session",
) -> dancer_schemas.Dancer:
    # feed data one to one into the dancer object
    dancer.name = dancer_data.name
    dancer.bio = dancer_data.bio
    dancer.date_of_birth = dancer_data.date_of_birth
    dancer.nationality = dancer_data.nationality
    dancer.based_in = dancer_data.based_in
    dancer.instagram = dancer_data.instagram
    dancer.youtube = dancer_data.youtube

    db.commit()
    db.refresh(dancer)

    return dancer_schemas.Dancer.model_validate(dancer)


# delete a specific dancer from the database
async def delete_dancer(dancer: dancer_models.Dancer, db: "Session"):
    db.delete(dancer)
    db.commit()
