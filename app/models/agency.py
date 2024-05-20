import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Agency(Base):
    __tablename__ = "agencies"

    id = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
        nullable=False,
    )
    name = Column(String(255), unique=True)
    website = Column(String(255), unique=True, nullable=True)
    instagram = Column(String(255), unique=True, nullable=True)
    contacts = relationship("Contact", back_populates="agency")

    def __repr__(self):
        return "<Agency: {name!r}>".format(name=self.name)
