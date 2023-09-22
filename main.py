from typing import TYPE_CHECKING, List
import fastapi

from sqlalchemy import orm
import schemas
import services

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


app = fastapi.FastAPI()

@app.post("/api/dancers/", response_model=schemas.Dancer)
async def create_dancer(
    dancer: schemas.CreateDancer, 
    db: orm.Session=fastapi.Depends(services.get_db),
):
    return await services.create_dancer(dancer=dancer, db=db)

@app.get("/api/dancers/", response_model=List[schemas.Dancer])
async def get_dancers(db: orm.Session=fastapi.Depends(services.get_db)):
    return await services.get_all_dancers(db=db)