import uuid

from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID

from app.database.database import Base


# models data classes define teh SQL tables
# while schemas data classes define the API that FastAPI uses the interact with the database
class Dancer(Base):
    __tablename__ = "dancers"

    id = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
        nullable=False,
    )
    name = Column(String(255), index=True)
    bio = Column(Text)
    nationality = Column(String(255))
    based_in = Column(String(255))
    instagram = Column(String, unique=True)
    youtube = Column(String(255), nullable=True)

    def __repr__(self):
        """returns strings representation of model instance"""
        return "<Dancer {name!r}>".format(name=self.name)
