from typing import List

from fastapi import Depends

from app.database import get_db
from app.models import dancer as dancer_models
from app.models import studio as studio_models
from app.schemas import studio as studio_schemas

from sqlalchemy.orm import Session

import uuid


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
        owners = (
            db.query(dancer_models.Dancer)
            .filter(dancer_models.Dancer.id.in_(studio.owner_ids))
            .all()
        )
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
    return studio


# delete a specific studio from the database
async def delete_studio(studio: studio_models.Studio, db: Session = Depends(get_db)):
    db.delete(studio)
    db.commit()


# update a specific studio in the database
async def update_studio(
    studio_id: uuid.UUID,
    studio_data: studio_schemas.UpdateStudio,
    db: Session = Depends(get_db),
) -> studio_schemas.Studio:

    # fetch the existing studio from the database
    studio = (
        db.query(studio_models.Studio)
        .filter(studio_models.Studio.id == studio_id)
        .first()
    )
    if not studio:
        raise Exception("Studio not found")

    # apply the updates to the studio, skipping any None values
    for k, v in studio_data.model_dump(exclude_unset=True).items():
        if k != "owner_ids" and hasattr(studio, k):
            setattr(studio, k, v)

    # if owner_ids are provided, update the studio's owners
    if studio_data.owner_ids:
        # query the database for the specified Dancer objects
        new_owners = (
            db.query(dancer_models.Dancer)
            .filter(dancer_models.Dancer.id.in_(studio_data.owner_ids))
            .all()
        )
        studio.owners = new_owners

    db.commit()
    db.refresh(studio)

    return studio_schemas.Studio.model_validate(studio)
