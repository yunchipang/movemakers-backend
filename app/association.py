from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


# studio & dancer
studio_owner_association = Table(
    "studio_owner_association",
    Base.metadata,
    Column("studio_id", UUID(as_uuid=True), ForeignKey("studios.id"), primary_key=True),
    Column("owner_id", UUID(as_uuid=True), ForeignKey("dancers.id"), primary_key=True),
)

# training & dancer
training_instructor_association = Table(
    "training_instructor_association",
    Base.metadata,
    Column(
        "training_id", UUID(as_uuid=True), ForeignKey("trainings.id"), primary_key=True
    ),
    Column(
        "instructor_id", UUID(as_uuid=True), ForeignKey("dancers.id"), primary_key=True
    ),
)


# crew & dancer
crew_leader_association = Table(
    "crew_leader_association",
    Base.metadata,
    Column("crew_id", UUID(as_uuid=True), ForeignKey("crews.id"), primary_key=True),
    Column("leader_id", UUID(as_uuid=True), ForeignKey("dancers.id"), primary_key=True),
)
crew_members_association = Table(
    "crew_members_association",
    Base.metadata,
    Column("crew_id", UUID(as_uuid=True), ForeignKey("crews.id"), primary_key=True),
    Column("member_id", UUID(as_uuid=True), ForeignKey("dancers.id"), primary_key=True),
)
