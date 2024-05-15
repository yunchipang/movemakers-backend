from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import contact as contact_exceptions
from app.models import contact as contact_models
from app.schemas import contact as contact_schemas


async def create_contact(
    contact: contact_schemas.CreateContact, db: Session = Depends(get_db)
) -> contact_schemas.Contact:
    # check contact email dupication
    existing_contact = (
        db.query(contact_models.Contact)
        .filter(contact_models.Contact.email == contact.email)
        .first()
    )
    if existing_contact:
        raise contact_exceptions.ContactDuplicateError

    contact = contact_models.Contact(**contact.model_dump())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact_schemas.Contact.model_validate(contact)
