from fastapi import FastAPI, Depends, HTTPException
from typing import Dict

from .routers import dancer, training, studio, crew

from sqlalchemy.orm import Session

from app.database import database
from app.models import user as user_models
from app.schemas import user as user_schemas
from app.services import user as user_services


app = FastAPI()
# register routers
app.include_router(dancer.router, prefix="/dancers", tags=["dancers"])
app.include_router(training.router, prefix="/trainings", tags=["trainings"])
app.include_router(studio.router, prefix="/studios", tags=["studios"])
app.include_router(crew.router, prefix="/crews", tags=["crews"])


@app.on_event("startup")
async def startup_event():
    # create tables if they do not exist yet
    database.create_tables()


@app.get("/")
async def get_root():
    return {"message": "Welcome to MoveMakers API"}


# signup
@app.post("/signup/", response_model=user_schemas.User)
async def signup(
    user: user_schemas.CreateUser,
    db: Session = Depends(database.get_db),
):
    # check duplicated email
    existing_user = user_services.get_user(email=user.email, db=db)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email is already in use.")

    """processes request to register user account"""
    user.hashed_password = user_models.User.hash_password(user.hashed_password)
    # return await user_services.create_user(user=user, db=db)
    created_user = await user_services.create_user(user=user, db=db)
    return created_user


# login
@app.post("/login/", response_model=Dict)
def login(
    payload: user_schemas.UserLogin,
    db: Session = Depends(database.get_db),
):
    """processes user's auth and returns a token on successful auth"""
    user = user_services.get_user(email=payload.email, db=db)
    if not user or not user.validate_password(payload.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid user credentials.",
        )
    return user.generate_token()
