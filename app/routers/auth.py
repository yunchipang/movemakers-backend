from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.database import get_db
from app.models import user as user_models
from app.schemas import user as user_schemas
from app.schemas import token as token_schemas
from app.services import user as user_services
from app.security import generate_token
from app.settings import get_settings


settings = get_settings()

router = APIRouter()


@router.post("/signup/", response_model=user_schemas.User)
async def signup(
    user: user_schemas.CreateUser,
    db: Session=Depends(get_db),
):
    """processes request to register user account"""
    existing_user = await user_services.get_user_by_email(email=user.email, db=db)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email is already in use.")
    
    user.hashed_password = user_models.User.hash_password(user.hashed_password)
    created_user = await user_services.create_user(user=user, db=db)
    return created_user


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session=Depends(get_db)
) -> token_schemas.Token:
    user = await user_services.authenticate_user(form_data.username, form_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    access_token = generate_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return token_schemas.Token(access_token=access_token, token_type="bearer")
