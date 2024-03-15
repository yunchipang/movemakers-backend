import uuid

from sqlalchemy import Column, Integer, String, ARRAY
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class Studio(Base):
    __tablename__ = "studios"

    id = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
        nullable=False,
    )
    name = Column(String, unique=True, index=True)
    address = Column(String)
    email = Column(String(255))
    phone = Column(String(255))
    opening_hours = Column(String)
    owner_ids = Column(ARRAY(UUID(as_uuid=True)))
    room_count = Column(Integer, nullable=True)
    founded_in = Column(Integer, nullable=True)
    instagram = Column(String(255), unique=True)
    youtube = Column(String(255), nullable=True)
    website = Column(String(255))

    def __repr__(self):
        """returns strings representation of model instance"""
        return "<Studio {name!r}>".format(name=self.name)
