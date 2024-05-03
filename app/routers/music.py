from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import music as music_schemas
from app.services import music as music_services

router = APIRouter()


@router.post("/", response_model=music_schemas.Music)
async def create_music(
    music: music_schemas.CreateMusic,
    db: Session = Depends(get_db),
):
    return await music_services.create_music(music=music, db=db)


@router.get("/", response_model=List[music_schemas.Music])
async def get_all_music(db: Session = Depends(get_db)):
    return await music_services.get_all_music(db=db)


@router.get("/{spotify_track_id}", response_model=music_schemas.Music)
async def get_music(spotify_track_id: str, db: Session = Depends(get_db)):
    music = await music_services.get_music(spotify_track_id=spotify_track_id, db=db)
    if music is None:
        raise HTTPException(status_code=404, detail="Music does not exist")
    return music


@router.put("/{spotify_track_id}", response_model=music_schemas.Music)
async def update_dancer(
    spotify_track_id: str,
    music_data: music_schemas.UpdateMusic,
    db: Session = Depends(get_db),
):
    updated_music = await music_services.update_music(
        spotify_track_id=spotify_track_id, music_data=music_data, db=db
    )
    if music_data is None:
        raise HTTPException(status_code=404, detail="Music not found")
    return updated_music


@router.delete("/{spotify_track_id}")
async def delete_music(spotify_track_id: str, db: Session = Depends(get_db)):
    music = await music_services.get_music(spotify_track_id=spotify_track_id, db=db)
    if music is None:
        raise HTTPException(status_code=404, detail="Music does not exist")

    await music_services.delete_music(music, db=db)
    return "Successfully deleted the music"