from typing import TYPE_CHECKING, List

from app.models import crew as crew_models
from app.schemas import crew as crew_schemas


if TYPE_CHECKING:
    from sqlalchemy.orm import Session


# create a crew instance in database using the crew data passed in
async def create_crew(
    crew: crew_schemas.CreateCrew, db: "Session"
) -> crew_schemas.Crew:

    crew = crew_models.Crew(**crew.model_dump())
    db.add(crew)
    db.commit()
    db.refresh(crew)
    return crew_schemas.Crew.model_validate(crew)


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
    crew_data: crew_schemas.CreateCrew,
    crew: crew_models.Crew,
    db: "Session",
) -> crew_schemas.Crew:
    # feed data one to one into the crew object
    crew.name = crew_data.name
    crew.bio = crew_data.bio
    crew.based_in = crew_data.based_in
    crew.founded_in = crew_data.founded_in
    crew.home_studio_id = crew_data.home_studio_id
    crew.styles = crew_data.styles
    crew.director_ids = crew_data.director_ids
    crew.captain_ids = crew_data.captain_ids
    crew.member_ids = crew_data.member_ids
    crew.rehearsal_schedules = crew_data.rehearsal_schedules
    crew.instagram = crew_data.instagram
    crew.youtube = crew_data.youtube
    crew.website = crew_data.website
    crew.is_active = crew_data.is_active

    db.commit()
    db.refresh(crew)

    return crew_schemas.Crew.model_validate(crew)
