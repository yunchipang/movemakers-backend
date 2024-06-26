from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import database
from app.routers import (
    agency,
    auth,
    choreography,
    contact,
    crew,
    dancer,
    music,
    studio,
    training,
    user,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    database.create_tables()
    yield  # this yield is necessary for the context manager to work correctly
    print("Shutting down...")  # optionally, handle any shutdown logic here


app = FastAPI(lifespan=lifespan)

# register routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(dancer.router, prefix="/dancers", tags=["dancers"])
app.include_router(training.router, prefix="/trainings", tags=["trainings"])
app.include_router(studio.router, prefix="/studios", tags=["studios"])
app.include_router(crew.router, prefix="/crews", tags=["crews"])
app.include_router(music.router, prefix="/music", tags=["music"])
app.include_router(choreography.router, prefix="/choreos", tags=["choreos"])
app.include_router(agency.router, prefix="/agencies", tags=["agencies"])
app.include_router(contact.router, prefix="/contacts", tags=["contacts"])


@app.get("/")
async def get_root():
    return {"message": "Welcome to MoveMakers API"}
