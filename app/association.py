from sqlalchemy import Column, ForeignKey, Table

from app.database import Base

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

crew_leader_association = Table(
    "crew_leader",
    Base.metadata,
    Column("crew_id", ForeignKey("crews.id"), primary_key=True),
    Column("leader_id", ForeignKey("dancers.id"), primary_key=True),
)

crew_member_association = Table(
    "crew_member",
    Base.metadata,
    Column("crew_id", ForeignKey("crews.id"), primary_key=True),
    Column("member_id", ForeignKey("dancers.id"), primary_key=True),
)

training_registration_association = Table(
    "training_registration",
    Base.metadata,
    Column("training_id", ForeignKey("trainings.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
)

choreography_choreographer_association = Table(
    "choreography_choreographer",
    Base.metadata,
    Column("choreography_id", ForeignKey("choreos.id"), primary_key=True),
    Column("choreographer_id", ForeignKey("dancers.id"), primary_key=True),
)
