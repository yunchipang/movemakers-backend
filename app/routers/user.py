from typing import Annotated

from fastapi import Depends, APIRouter

from app.schemas import user as user_schemas
from app.services import user as user_services

router = APIRouter()


@router.get("/me")
async def read_users_me(
    current_user: Annotated[
        user_schemas.User, Depends(user_services.get_current_active_user)
    ],
):
    return current_user
