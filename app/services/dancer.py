from typing import TYPE_CHECKING, List

from app.models import dancer as dancer_models
from app.schemas import dancer as dancer_schemas

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


# create a dancer instance in database using the dancer data passed in
async def create_dancer(dancer: dancer_schemas.CreateDancer, db: "Session") -> dancer_schemas.Dancer:
    dancer = dancer_models.Dancer(**dancer.dict())
    db.add(dancer)
    db.commit()
    db.refresh(dancer)
    return dancer_schemas.Dancer.from_orm(dancer)

# query database to get all dancers
async def get_all_dancers(db: "Session") -> List[dancer_schemas.Dancer]:
    dancers = db.query(dancer_models.Dancer).all()
    return list(map(dancer_schemas.Dancer.from_orm, dancers))

# query database for a specific dancer with the dancer id
async def get_dancer(dancer_id: int, db: "Session"):
    dancer = db.query(dancer_models.Dancer).filter(dancer_models.Dancer.id == dancer_id).first()
    return dancer

# delete a specific dancer from the database
async def delete_dancer(dancer: dancer_models.Dancer, db: "Session"):
    db.delete(dancer)
    db.commit()

# update a specific dancer in the database
async def update_dancer(
        dancer_data: dancer_schemas.CreateDancer, dancer: dancer_models.Dancer, db: "Session"
) -> dancer_schemas.Dancer:
    # feed data one to one into the dancer object
    dancer.name = dancer_data.name
    dancer.instagram_handle = dancer_data.instagram_handle
    dancer.rols = dancer_data.roles
    dancer.styles = dancer_data.styles

    db.commit()
    db.refresh(dancer)

    return dancer_schemas.Dancer.from_orm(dancer)
