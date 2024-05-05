from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import music as music_exceptions
from app.models import music as music_models
from app.schemas import music as music_schemas


async def create_music(
    music: music_schemas.CreateMusic, db: Session = Depends(get_db)
) -> music_schemas.Music:
    music = music_models.Music(**music.model_dump())
    db.add(music)
    db.commit()
    db.refresh(music)
    return music_schemas.Music.model_validate(music)


async def get_all_music(db: Session = Depends(get_db)) -> List[music_schemas.Music]:
    musics = db.query(music_models.Music).all()
    return [music_schemas.Music.model_validate(music) for music in musics]


async def get_music(spotify_track_id: str, db: Session = Depends(get_db)):
    music = (
        db.query(music_models.Music)
        .filter(music_models.Music.spotify_track_id == spotify_track_id)
        .first()
    )
    if not music:
        raise music_exceptions.MusicNotFoundError(spotify_track_id)
    return music


async def update_music(
    spotify_track_id: str,
    music_data: music_schemas.UpdateMusic,
    db: Session = Depends(get_db),
) -> music_schemas.Music:

    music = (
        db.query(music_models.Music)
        .filter(music_models.Music.spotify_track_id == spotify_track_id)
        .first()
    )
    if not music:
        raise Exception("Music not found")

    for k, v in music_data.model_dump(exclude_unset=True).items():
        if hasattr(music, k):
            setattr(music, k, v)

    db.commit()
    db.refresh(music)

    return music_schemas.Music.model_validate(music)


async def delete_music(music: music_models.Music, db: Session = Depends(get_db)):
    db.delete(music)
    db.commit()
