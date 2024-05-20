from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import agency as agency_exceptions
from app.models import agency as agency_models
from app.schemas import agency as agency_schemas


async def create_agency(
    agency: agency_schemas.CreateAgency, db: Session = Depends(get_db)
) -> agency_schemas.Agency:

    # check if an agency with the same name, website, or instagram handle already exists
    existing_agency = (
        db.query(agency_models.Agency)
        .filter(
            (agency_models.Agency.name == agency.name)
            | (agency_models.Agency.website == agency.website)
            | (agency_models.Agency.instagram == agency.instagram)
        )
        .first()
    )
    if existing_agency:
        raise agency_exceptions.AgencyDuplicateError

    new_agency = agency_models.Agency(**agency.model_dump())

    db.add(new_agency)
    db.commit()
    db.refresh(new_agency)

    # debug
    print("!!!!!! new_agency !!!!!!!")
    for column in agency_models.Agency.__table__.columns:
        attr_name = column.name
        attr_value = getattr(new_agency, attr_name, None)
        print(f"{attr_name}: {attr_value}")

    return agency_schemas.Agency.model_validate(new_agency)


async def get_all_agencies(
    db: Session = Depends(get_db),
) -> List[agency_schemas.Agency]:
    agencies = db.query(agency_models.Agency).all()
    return [agency_schemas.Agency.model_validate(agency) for agency in agencies]
