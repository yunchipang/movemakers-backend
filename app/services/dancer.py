import uuid
from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import dancer as dancer_exceptions
from app.models import dancer as dancer_models
from app.schemas import dancer as dancer_schemas


# create a dancer instance in database using the dancer data passed in
async def create_dancer(
    dancer: dancer_schemas.CreateDancer, db: Session = Depends(get_db)
) -> dancer_schemas.Dancer:
    dancer = dancer_models.Dancer(**dancer.model_dump())
    db.add(dancer)
    db.commit()
    db.refresh(dancer)
    return dancer_schemas.Dancer.model_validate(dancer)


# query database to get all dancers
async def get_all_dancers(db: Session = Depends(get_db)) -> List[dancer_schemas.Dancer]:
    dancers = db.query(dancer_models.Dancer).all()
    return [dancer_schemas.Dancer.model_validate(dancer) for dancer in dancers]


# query database for a specific dancer with the dancer id
async def get_dancer(dancer_id: str, db: Session = Depends(get_db)):
    dancer = (
        db.query(dancer_models.Dancer)
        .filter(dancer_models.Dancer.id == dancer_id)
        .first()
    )
    if not dancer:
        raise dancer_exceptions.DancerNotFoundError
    return dancer


# update a specific dancer in the database
async def update_dancer(
    dancer_id: uuid.UUID,
    dancer_data: dancer_schemas.UpdateDancer,
    db: Session = Depends(get_db),
) -> dancer_schemas.Dancer:
    dancer = await get_dancer(dancer_id=dancer_id, db=db)
    for k, v in dancer_data.model_dump(exclude_unset=True).items():
        if hasattr(dancer, k):
            setattr(dancer, k, v)

    db.commit()
    db.refresh(dancer)

    return dancer_schemas.Dancer.model_validate(dancer)


# delete a specific dancer from the database
async def delete_dancer(dancer: dancer_models.Dancer, db: Session = Depends(get_db)):
    db.delete(dancer)
    db.commit()
