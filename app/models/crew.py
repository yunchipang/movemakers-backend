import uuid

from sqlalchemy import ARRAY, Boolean, Column, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base
from app.enums.style import Style
from app.association import crew_members_association


class Crew(Base):
    __tablename__ = "crews"

    id = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
        nullable=False,
    )
    name = Column(String(255), index=True)
    bio = Column(Text)
    based_in = Column(String(255))
    founded_in = Column(Integer, nullable=True)
    styles = Column(ARRAY(Enum(Style)))
    rehearsal_schedules = Column(Text, nullable=True)
    instagram = Column(String(255), unique=True)
    youtube = Column(String(255), nullable=True)
    website = Column(String(255))
    is_active = Column(Boolean, default=True)

    home_studio_id = Column(UUID(as_uuid=True), ForeignKey("studios.id"), nullable=True)
    home_studio = relationship("Studio", back_populates="homed_crews")
    
    leader_id = Column(UUID(as_uuid=True), ForeignKey("dancers.id"))
    leader = relationship("Dancer", back_populates="lead_crews")
    members = relationship("Dancer", secondary=crew_members_association)

    def __repr__(self):
        """returns strings representation of model instance"""
        return f"<Crew {self.name!r}>"
