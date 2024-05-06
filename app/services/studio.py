import uuid
from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import studio as studio_exceptions
from app.models import studio as studio_models
from app.schemas import studio as studio_schemas
from app.services import dancer as dancer_services


# create a studio instance in database using the studio data passed in
async def create_studio(
    studio: studio_schemas.CreateStudio, db: Session = Depends(get_db)
) -> studio_schemas.Studio:

    # exclude owner_ids from studio
    studio_data = studio.model_dump(exclude={"owner_ids"})

    # create the studio instance without the owners
    new_studio = studio_models.Studio(**studio_data)
    db.add(new_studio)
    db.flush()  # flush to assign an ID to new_studio without committing the transaction

    # associate owners with the new studio if owner_ids were provided
    if studio.owner_ids:
        owners = []
        for owner_id in studio.owner_ids:
            owner = await dancer_services.get_dancer(owner_id, db=db)
            owners.append(owner)
        new_studio.owners = owners

    db.commit()
    db.refresh(new_studio)
    return studio_schemas.Studio.model_validate(new_studio)


# query database to get all studios
async def get_all_studios(db: Session = Depends(get_db)) -> List[studio_schemas.Studio]:
    studios = db.query(studio_models.Studio).all()
    return [studio_schemas.Studio.model_validate(studio) for studio in studios]


# query database for a specific studio with the studio id
async def get_studio(studio_id: str, db: Session = Depends(get_db)):
    studio = (
        db.query(studio_models.Studio)
        .filter(studio_models.Studio.id == studio_id)
        .first()
    )
    if not studio:
        raise studio_exceptions.StudioNotFoundError(studio_id)
    return studio


# update a specific studio in the database
async def update_studio(
    studio_id: uuid.UUID,
    studio_data: studio_schemas.UpdateStudio,
    db: Session = Depends(get_db),
) -> studio_schemas.Studio:
    studio = await get_studio(studio_id=studio_id, db=db)
    for k, v in studio_data.model_dump(exclude_unset=True).items():
        if k != "owner_ids" and hasattr(studio, k):
            setattr(studio, k, v)

    if studio_data.owner_ids:
        new_owners = []
        for owner_id in studio_data.owner_ids:
            owner = await dancer_services.get_dancer(owner_id, db=db)
            new_owners.append(owner)
        studio.owners = new_owners

    db.commit()
    db.refresh(studio)

    return studio_schemas.Studio.model_validate(studio)


# delete a specific studio from the database
async def delete_studio(studio: studio_models.Studio, db: Session = Depends(get_db)):
    db.delete(studio)
    db.commit()
