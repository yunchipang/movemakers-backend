from pydantic import BaseModel
from datetime import datetime
from models.person import Person
from enums.style import Style
from enums.level import Level


class Choreo(BaseModel):
    choreographer: Person
    music: str
    style: list[Style]
    level: Level
    video: str
    created_at: datetime.now()