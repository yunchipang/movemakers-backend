from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import contact as contact_exceptions
from app.schemas import contact as contact_schemas
from app.services import contact as contact_services

router = APIRouter()


@router.post("/", response_model=contact_schemas.Contact)
async def create_contact(
    contact: contact_schemas.CreateContact,
    db: Session = Depends(get_db),
):
    try:
        new_contact = await contact_services.create_contact(contact=contact, db=db)
    except contact_exceptions.ContactDuplicateError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    return new_contact
