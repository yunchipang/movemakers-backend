from app.database import Base
from sqlalchemy import Column, ForeignKey, Table

studio_owner_association = Table(
    "studio_owner",
    Base.metadata,
    Column("studio_id", ForeignKey("studios.id"), primary_key=True),
    Column("owner_id", ForeignKey("dancers.id"), primary_key=True),
)

training_instructor_association = Table(
    "training_instructor",
    Base.metadata,
    Column("training_id", ForeignKey("trainings.id"), primary_key=True),
    Column("instructor_id", ForeignKey("dancers.id"), primary_key=True),
)
