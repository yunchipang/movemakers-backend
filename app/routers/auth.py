from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import token as token_schemas
from app.schemas import user as user_schemas
from app.security import generate_token, hash_password
from app.services import user as user_services
from app.settings import get_settings

settings = get_settings()

router = APIRouter()


@router.post(
    "/signup/", response_model=user_schemas.User, status_code=status.HTTP_201_CREATED
)
async def signup(
    user: user_schemas.CreateUser,
    db: Session = Depends(get_db),
):
    """processes request to register a user account by checking for duplicate username and email."""
    # check if the username and/or email is already in use
    existing_user_by_username = await user_services.get_user_by_username(
        username=user.username, db=db
    )
    if existing_user_by_username:
        raise HTTPException(status_code=400, detail="Username is already in use.")

    existing_user_by_email = await user_services.get_user_by_email(
        email=user.email, db=db
    )
    if existing_user_by_email:
        raise HTTPException(status_code=400, detail="Email is already in use.")

    hashed_password = hash_password(user.hashed_password)
    hashed_password_bytes = (
        hashed_password.encode("utf-8")
        if isinstance(hashed_password, str)
        else hashed_password
    )
    user.hashed_password = hashed_password_bytes
    created_user = await user_services.create_user(user=user, db=db)
    return created_user


@router.post("/login/")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> token_schemas.Token:
    user = await user_services.authenticate_user(
        form_data.username, form_data.password, db=db
    )
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
