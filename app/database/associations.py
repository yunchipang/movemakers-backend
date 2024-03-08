from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.database.database import Base


# association table for the many-to-many relationships
# crew's directors, captains, members are dancers
crew_director_association = Table(
    "crew_director_association",
    Base.metadata,
    Column("crew_id", UUID(as_uuid=True), ForeignKey("crews.id")),
    Column("dancer_id", UUID(as_uuid=True), ForeignKey("dancers.id")),
)

crew_captain_association = Table(
    "crew_captain_association",
    Base.metadata,
    Column("crew_id", UUID(as_uuid=True), ForeignKey("crews.id")),
    Column("dancer_id", UUID(as_uuid=True), ForeignKey("dancers.id")),
)

crew_member_association = Table(
    "crew_member_association",
    Base.metadata,
    Column("crew_id", UUID(as_uuid=True), ForeignKey("crews.id")),
    Column("dancer_id", UUID(as_uuid=True), ForeignKey("dancers.id")),
)

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
