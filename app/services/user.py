from typing import TYPE_CHECKING

from app.models import user as user_models
from app.schemas import user as user_schemas

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


async def create_user(user: user_schemas.CreateUser, db: "Session") -> user_schemas.User:
    user = user_models.User(**user.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user_schemas.User.from_orm(user)

async def get_user(email: str, db: "Session"):
    return db.query(user_models.User).filter(user_models.User.email == email).first()
