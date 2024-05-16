import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base
from app.association import dancer_contact_association

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    type = Column(String(255))
    name = Column(String(255), nullable=True)
    email = Column(String(255))
    phone = Column(String(255), nullable=True)

    # fk to the agencies table
    agency_id = Column(UUID(as_uuid=True), ForeignKey("agencies.id"), nullable=False)
    agency = relationship("Agency", back_populates="contacts")

    # fk to the dancers table
    dancers = relationship(
        "Dancer",
        secondary=dancer_contact_association,
        back_populates="contacts"
    )

    def __repr__(self):
        return "<Contact: {email!r}>".format(email=self.email)
