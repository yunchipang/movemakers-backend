from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session
import uuid
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


async def get_all_contacts(
    db: Session = Depends(get_db),
) -> List[contact_schemas.Contact]:
    contacts = db.query(contact_models.Contact).all()
    return [contact_schemas.Contact.model_validate(contact) for contact in contacts]

async def get_contact(contact_id: str, db: Session = Depends(get_db)):
    try:
        if isinstance(contact_id, uuid.UUID):
            valid_contact_id = contact_id
        else:
            valid_contact_id = uuid.UUID(str(contact_id))
        contact = (
            db.query(contact_models.Contact)
            .filter(contact_models.Contact.id == valid_contact_id)
            .first()
        )
    except ValueError:
        raise contact_exceptions.InvalidContactIdError

    if not contact:
        raise contact_exceptions.ContactNotFoundError
    return contact

async def get_contacts(contact_ids: List[str], db: Session = Depends(get_db)):
    contacts = []
    for contact_id in contact_ids:
        contact = await get_contact(contact_id, db=db)
        contacts.append(contact)
    return contacts
