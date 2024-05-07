import uuid
from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import choreography as choreography_exceptions
from app.models import choreography as choreography_models
from app.schemas import choreography as choreography_schemas
from app.services import dancer as dancer_services
from app.services import music as music_services


async def create_choreography(
    choreography: choreography_schemas.CreateChoreography, db: Session = Depends(get_db)
) -> choreography_schemas.Choreography:
    choreo_data = choreography.model_dump(exclude={"music_id", "choreographer_ids"})

    new_choreo = choreography_models.Choreography(**choreo_data)
    db.add(new_choreo)
    db.flush()

    # assign music for this choreography
    music = await music_services.get_music(choreography.music_id, db=db)
    new_choreo.music = music

    # assign choreographers for this choreography
    choreographers = await dancer_services.get_dancers(choreography.choreographer_ids, db=db)
    new_choreo.choreographers = choreographers

    db.commit()
    db.refresh(new_choreo)

    return choreography_schemas.Choreography.model_validate(new_choreo)


async def get_all_choreos(
    db: Session = Depends(get_db),
) -> List[choreography_schemas.Choreography]:
    choreos = db.query(choreography_models.Choreography).all()
    return [
        choreography_schemas.Choreography.model_validate(choreo) for choreo in choreos
    ]


async def get_choreography(choreo_id: str, db: Session = Depends(get_db)):
    choreo = (
        db.query(choreography_models.Choreography)
        .filter(choreography_models.Choreography.id == choreo_id)
        .first()
    )
    if not choreo:
        raise choreography_exceptions.ChoreographyNotFoundError
    return choreo


async def update_choreography(
    choreo_id: uuid.UUID,
    choreo_data: choreography_schemas.UpdateChoreography,
    db: Session = Depends(get_db),
) -> choreography_schemas.Choreography:
    choreo = await get_choreography(choreo_id, db=db)
    for k, v in choreo_data.model_dump(exclude_unset=True).items():
        if k != "music_id" and k != "choreographer_ids" and hasattr(choreo, k):
            setattr(choreo, k, v)

    if choreo_data.music_id:
        new_music = await music_services.get_music(choreo_data.music_id, db=db)
        choreo.music = new_music

    if choreo_data.choreographer_ids:
        new_choreographers = await dancer_services.get_dancers(choreo_data.choreographer_ids, db=db)
        choreo.choreographers = new_choreographers

    db.commit()
    db.refresh(choreo)

    return choreography_schemas.Choreography.model_validate(choreo)


async def delete_choreography(
    choreography: choreography_models.Choreography, db: Session = Depends(get_db)
):
    db.delete(choreography)
    db.commit()
