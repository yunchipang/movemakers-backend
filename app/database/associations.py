from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.database.database import Base

# studio's owners are dancers
studio_owner_association = Table(
    "studio_owner_association",
    Base.metadata,
    Column("studio_id", UUID(as_uuid=True), ForeignKey("studios.id")),
    Column("dancer_id", UUID(as_uuid=True), ForeignKey("dancers.id")),
)

# training's instructors are dancers
training_instructor_association = Table(
    "training_instructor_association",
    Base.metadata,
    Column("training_id", UUID(as_uuid=True), ForeignKey("trainings.id")),
    Column("dancer_id", UUID(as_uuid=True), ForeignKey("dancers.id")),
)
