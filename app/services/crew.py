from typing import TYPE_CHECKING, List

from app.models import crew as crew_models
from app.models import dancer as dancer_models
from app.models import studio as studio_models
from app.schemas import crew as crew_schemas


import uuid

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


# create a crew instance in database using the crew data passed in
async def create_crew(
    crew: crew_schemas.CreateCrew, db: "Session"
) -> crew_schemas.Crew:
    # home_studio_id: Optional[uuid.UUID] = crew.home_studio_id
    # leader_ids: List[uuid.UUID] = crew.leader_ids
    # member_ids: List[uuid.UUID] = crew.member_ids
    crew_data = crew.model_dump(exclude={"home_studio_id", "leader_ids", "member_ids"})

    new_crew = crew_models.Crew(**crew_data)
    db.add(new_crew)
    db.flush()

    if crew.home_studio_id:
        home_studio = (
            db.query(studio_models.Studio)
            .filter(studio_models.Studio.id == crew.home_studio_id)
            .first()
        )
        new_crew.home_studio = home_studio
    leaders = (
        db.query(dancer_models.Dancer)
        .filter(dancer_models.Dancer.id.in_(crew.leader_ids))
        .all()
    )
    new_crew.leaders = leaders
    members = (
        db.query(dancer_models.Dancer)
        .filter(dancer_models.Dancer.id.in_(crew.member_ids))
        .all()
    )
    new_crew.members = members

    db.commit()
    db.refresh(new_crew)
    return crew_schemas.Crew.model_validate(new_crew)


# query database to get all crews
async def get_all_crews(db: "Session") -> List[crew_schemas.Crew]:
    crews = db.query(crew_models.Crew).all()
    return [crew_schemas.Crew.model_validate(crew) for crew in crews]


# query database for a specific crew with the crew id
async def get_crew(crew_id: str, db: "Session"):
    crew = db.query(crew_models.Crew).filter(crew_models.Crew.id == crew_id).first()
    return crew


# delete a specific crew from the database
async def delete_crew(crew: crew_models.Crew, db: "Session"):
    db.delete(crew)
    db.commit()


# update a specific crew in the database
async def update_crew(
    crew_id: uuid.UUID,
    crew_data: crew_schemas.UpdateCrew,
    db: "Session",
) -> crew_schemas.Crew:

    # fetch exisiting crew by id from the database
    crew = db.query(crew_models.Crew).filter(crew_models.Crew.id == crew_id).first()
    if not crew:
        raise Exception("Crew not found")

    for k, v in crew_data.model_dump(exclude_unset=True).items():
        if (
            k != "home_studio_id"
            and k != "leader_ids"
            and k != "member_ids"
            and hasattr(crew, k)
        ):
            setattr(crew, k, v)
    # set home_studio, leaders and members
    if crew_data.home_studio_id:
        new_home_studio = (
            db.query(crew_models.Crew)
            .filter(crew_models.Crew.id == crew_data.home_studio_id)
            .first()
        )
        crew.home_studio = new_home_studio
    if crew_data.leader_ids:
        new_leaders = (
            db.query(crew_models.Crew)
            .filter(crew_models.Crew.id.in_(crew_data.leader_ids))
            .all()
        )
        crew.leaders = new_leaders
    if crew_data.member_ids:
        new_members = (
            db.query(crew_models.Crew)
            .filter(crew_models.Crew.id.in_(crew_data.member_ids))
            .all()
        )
        crew.members = new_members

    db.commit()
    db.refresh(crew)

    return crew_schemas.Crew.model_validate(crew)
