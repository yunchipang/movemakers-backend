from typing import TYPE_CHECKING, List

from app.models import dancer as dancer_models
from app.models import studio as studio_models
from app.schemas import studio as studio_schemas

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

import uuid


# create a studio instance in database using the studio data passed in
async def create_studio(
    studio: studio_schemas.CreateStudio, db: "Session"
) -> studio_schemas.Studio:
    # studio = studio_models.Studio(**studio.model_dump())

    # exclude owner_ids from studio
    owner_ids: List[uuid.UUID] = studio.owner_ids if studio.owner_ids else []
    studio_data = studio.dict(exclude={"owner_ids"})

    # create the studio instance without the owners
    new_studio = studio_models.Studio(**studio_data)
    db.add(new_studio)
    db.flush()  # flush to assign an ID to new_studio without committing the transaction

    # associate owners with the new studio if owner_ids were provided
    if owner_ids:
        owners = (
            db.query(dancer_models.Dancer)
            .filter(dancer_models.Dancer.id.in_(owner_ids))
            .all()
        )
        new_studio.owners = owners

    db.commit()
    db.refresh(new_studio)
    return studio_schemas.Studio.model_validate(new_studio)


# query database to get all studios
async def get_all_studios(db: "Session") -> List[studio_schemas.Studio]:
    studios = db.query(studio_models.Studio).all()
    return [studio_schemas.Studio.model_validate(studio) for studio in studios]


# query database for a specific studio with the studio id
async def get_studio(studio_id: str, db: "Session"):
    studio = (
        db.query(studio_models.Studio)
        .filter(studio_models.Studio.id == studio_id)
        .first()
    )
    return studio


# delete a specific studio from the database
async def delete_studio(studio: studio_models.Studio, db: "Session"):
    db.delete(studio)
    db.commit()


# update a specific studio in the database
async def update_studio(
    studio_data: studio_schemas.CreateStudio,
    studio: studio_models.Studio,
    db: "Session",
) -> studio_schemas.Studio:
    # feed data one to one into the studio object
    studio.name = studio_data.name
    studio.address = studio_data.address
    studio.email = studio_data.email
    studio.phone = studio_data.phone
    studio.opening_hours = studio_data.opening_hours
    studio.room_count = studio_data.room_count
    studio.founded_in = studio_data.founded_in
    studio.instagram = studio_data.instagram
    studio.youtube = studio_data.youtube
    studio.website = studio_data.website
    studio.owners = studio_data.owners

    db.commit()
    db.refresh(studio)

    return studio_schemas.Studio.model_validate(studio)
