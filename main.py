from typing import TYPE_CHECKING
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