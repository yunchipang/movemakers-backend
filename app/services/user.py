from typing import Annotated

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import user as user_models
from app.schemas import token as token_schemas
from app.schemas import user as user_schemas
from app.security import oauth2_scheme, validate_password
from app.settings import get_settings

settings = get_settings()


async def create_user(
    user: user_schemas.CreateUser, db: Session = Depends(get_db)
) -> user_schemas.User:
    user = user_models.User(**user.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user_schemas.User.model_validate(user)


async def get_user_by_username(username: str, db: Session = Depends(get_db)):
    return (
        db.query(user_models.User).filter(user_models.User.username == username).first()
    )


async def get_user_by_email(email: str, db: Session = Depends(get_db)):
    return db.query(user_models.User).filter(user_models.User.email == email).first()


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = token_schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user_by_username(username=token_data.username, db=db)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[user_schemas.User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def authenticate_user(
    username: str, password: str, db: Session = Depends(get_db)
):
    user = await get_user_by_username(username, db)
    if not user:
        return False
    if not validate_password(password, user.hashed_password):
        return False
    return user
