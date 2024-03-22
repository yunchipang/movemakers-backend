from fastapi import FastAPI
from .routers import dancer, training, studio, crew, auth

from app import database


app = FastAPI()
# register routers
app.include_router(dancer.router, prefix="/dancers", tags=["dancers"])
app.include_router(training.router, prefix="/trainings", tags=["trainings"])
app.include_router(studio.router, prefix="/studios", tags=["studios"])
app.include_router(crew.router, prefix="/crews", tags=["crews"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])


@app.on_event("startup")
async def startup_event():
    # create tables if they do not exist yet
    database.create_tables()


@app.get("/")
async def get_root():
    return {"message": "Welcome to MoveMakers API"}
