import uuid
from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import crew as crew_models
from app.schemas import crew as crew_schemas
from app.services import studio as studio_services
from app.services import dancer as dancer_services
from app.exceptions import crew as crew_exceptions

# create a crew instance in database using the crew data passed in
async def create_crew(
    crew: crew_schemas.CreateCrew, db: Session = Depends(get_db)
) -> crew_schemas.Crew:
    crew_data = crew.model_dump(exclude={"home_studio_id", "leader_ids", "member_ids"})

    new_crew = crew_models.Crew(**crew_data)
    db.add(new_crew)
    db.flush()

    # get & assign home_studio
    if crew.home_studio_id:
        home_studio = await studio_services.get_studio(crew.home_studio_id, db=db)
        new_crew.home_studio = home_studio
    # get & assign leaders
    leaders = []
    for leader_id in crew.leader_ids:
        leader = await dancer_services.get_dancer(leader_id, db=db)
        leaders.append(leader)
    new_crew.leaders = leaders
    # get & assign memebers
    members = []
    for member_id in crew.member_ids:
        member = await dancer_services.get_dancer(member_id, db=db)
        members.append(member)
    new_crew.members = members

    db.commit()
    db.refresh(new_crew)
    return crew_schemas.Crew.model_validate(new_crew)


# query database to get all crews
async def get_all_crews(db: Session = Depends(get_db)) -> List[crew_schemas.Crew]:
    crews = db.query(crew_models.Crew).all()
    return [crew_schemas.Crew.model_validate(crew) for crew in crews]


# query database for a specific crew with the crew id
async def get_crew(crew_id: str, db: Session = Depends(get_db)):
    crew = db.query(crew_models.Crew).filter(crew_models.Crew.id == crew_id).first()
    if not crew:
        raise crew_exceptions.CrewNotFoundError
    return crew


# update a specific crew in the database
async def update_crew(
    crew_id: uuid.UUID,
    crew_data: crew_schemas.UpdateCrew,
    db: Session = Depends(get_db),
) -> crew_schemas.Crew:

    crew = await get_crew(crew_id=crew_id, db=db)
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
        new_home_studio = await studio_services.get_studio(crew_data.home_studio_id, db=db)
        crew.home_studio = new_home_studio
    if crew_data.leader_ids:
        new_leaders = []
        for leader_id in crew.leader_ids:
            leader = await dancer_services.get_dancer(leader_id, db=db)
            new_leaders.append(leader)
        crew.leaders = new_leaders
    if crew_data.member_ids:
        new_members = []
        for member_id in crew.member_ids:
            member = await dancer_services.get_dancer(member_id, db=db)
            new_members.append(member)
        crew.members = new_members

    db.commit()
    db.refresh(crew)

    return crew_schemas.Crew.model_validate(crew)


# delete a specific crew from the database
async def delete_crew(crew: crew_models.Crew, db: Session = Depends(get_db)):
    db.delete(crew)
    db.commit()