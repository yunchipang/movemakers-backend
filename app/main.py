from typing import List, Dict

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from app import database
from app.models import user as user_models
from app.schemas import dancer as dancer_schemas
from app.schemas import user as user_schemas
from app.services import dancer as dancer_services
from app.services import user as user_services

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    # create tables if they do not exist yet
    database.add_tables()

@app.get("/")
async def get_root():
    return {"message": "Welcome to MoveMakers API"}

# signup endpoint
@app.post("/signup/", response_model=user_schemas.User)
async def signup(
    user: user_schemas.CreateUser,
    db: Session=Depends(database.get_db),
):
    # check duplicated email
    existing_user = user_services.get_user(email=user.email, db=db)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email is already in use.")
    
    """processes request to register user account"""
    user.hashed_password = user_models.User.hash_password(user.hashed_password)
    return await user_services.create_user(user=user, db=db)

# login endpoint
@app.post("/login/", response_model=Dict)
def login(
    payload: user_schemas.UserLogin,
    db: Session=Depends(database.get_db),
):
    """processes user's auth and returns a token on successful auth"""
    user = user_services.get_user(email=payload.email, db=db)
    if not user or not user.validate_password(payload.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid user credentials.",
        )
    return user.generate_token()

# dancers endpoints
@app.post("/dancers/", response_model=dancer_schemas.Dancer)
async def create_dancer(
    dancer: dancer_schemas.CreateDancer, 
    db: Session=Depends(database.get_db),
):
    return await dancer_services.create_dancer(dancer=dancer, db=db)

@app.get("/dancers/", response_model=List[dancer_schemas.Dancer])
async def get_dancers(db: Session=Depends(database.get_db)):
    return await dancer_services.get_all_dancers(db=db)

@app.get("/dancers/{dancer_id}", response_model=dancer_schemas.Dancer)
async def get_dancer(
    dancer_id: int, 
    db: Session=Depends(database.get_db)
):
    dancer = await dancer_services.get_dancer(dancer_id=dancer_id, db=db)
    print("dancer=", dancer)
    if dancer is None:
        raise HTTPException(status_code=404, detail="Dancer does not exist")
    
    return dancer

@app.delete("/dancers/{dancer_id}")
async def delete_dancer(
    dancer_id: int,
    db: Session=Depends(database.get_db)
):
    dancer = await dancer_services.get_dancer(dancer_id=dancer_id, db=db)
    if dancer is None:
        raise HTTPException(status_code=404, detail="Dancer does not exist")

    await dancer_services.delete_dancer(dancer, db=db)
    return "successfully deleted the dancer"

@app.put("/dancers/{dancer_id}", response_model=dancer_schemas.Dancer)
async def update_dancer(
    dancer_id: int,
    dancer_data: dancer_schemas.CreateDancer,
    db: Session=Depends(database.get_db)
):
    dancer = await dancer_services.get_dancer(dancer_id=dancer_id, db=db)
    if dancer is None:
        raise HTTPException(status_code=404, detail="Dancer does not exist")

    return await dancer_services.update_dancer(dancer_data=dancer_data, dancer=dancer, db=db)
