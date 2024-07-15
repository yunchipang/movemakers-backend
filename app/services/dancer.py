import uuid
from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import dancer as dancer_exceptions
from app.models import dancer as dancer_models
from app.schemas import dancer as dancer_schemas
from app.services import contact as contact_services


# create a dancer instance in database using the dancer data passed in
async def create_dancer(
    dancer: dancer_schemas.CreateDancer, db: Session = Depends(get_db)
) -> dancer_schemas.Dancer:
    dancer_data = dancer.model_dump(exclude={"contact_ids"})

    new_dancer = dancer_models.Dancer(**dancer_data)
    db.add(new_dancer)
    db.flush()

    # associate contacts to this dancer
    if dancer.contact_ids:
        contacts = await contact_services.get_contacts(dancer.contact_ids, db=db)
        new_dancer.contacts = contacts

    db.commit()
    db.refresh(new_dancer)
    return dancer_schemas.Dancer.model_validate(new_dancer)


# query database to get all dancers
async def get_all_dancers(db: Session = Depends(get_db)) -> List[dancer_schemas.Dancer]:
    dancers = db.query(dancer_models.Dancer).all()
    return [dancer_schemas.Dancer.model_validate(dancer) for dancer in dancers]


# query database for a specific dancer with the dancer id
async def get_dancer(dancer_id: str, db: Session = Depends(get_db)):
    try:
        # ensure the UUID is correctly formatted before querying
        if isinstance(dancer_id, uuid.UUID):
            valid_dancer_id = dancer_id
        else:
            valid_dancer_id = uuid.UUID(str(dancer_id))
        dancer = (
            db.query(dancer_models.Dancer)
            .filter(dancer_models.Dancer.id == valid_dancer_id)
            .first()
        )
    except ValueError:
        raise dancer_exceptions.InvalidDancerIdError

    if not dancer:
        raise dancer_exceptions.DancerNotFoundError
    return dancer


async def get_dancers(dancer_ids: List[str], db: Session = Depends(get_db)):
    dancers = []
    for dancer_id in dancer_ids:
        dancer = await get_dancer(dancer_id, db=db)
        dancers.append(dancer)
    return dancers


# update a specific dancer in the database
async def update_dancer(
    dancer_id: uuid.UUID,
    dancer_data: dancer_schemas.UpdateDancer,
    db: Session = Depends(get_db),
) -> dancer_schemas.Dancer:
    dancer = await get_dancer(dancer_id=dancer_id, db=db)
    for k, v in dancer_data.model_dump(exclude_unset=True).items():
        if k != "contact_ids" and hasattr(dancer, k):
            setattr(dancer, k, v)

    # handle new contacts
    if dancer_data.contact_ids:
        new_contacts = await contact_services.get_contacts(
            dancer_data.contact_ids, db=db
        )
        dancer.contacts = new_contacts

    db.commit()
    db.refresh(dancer)

    return dancer_schemas.Dancer.model_validate(dancer)


# delete a specific dancer from the database
async def delete_dancer(dancer: dancer_models.Dancer, db: Session = Depends(get_db)):
    db.delete(dancer)
    db.commit()
