from sqlalchemy import Column, Integer, String
from sqlalchemy.types import ARRAY

from app.database import Base


class Dancer(Base):
    __tablename__ = "dancers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    instagram_handle = Column(String, unique=True, index=True)
    roles = Column(ARRAY(String), default=[], nullable=True) # use enum RoleEnum
    styles = Column(ARRAY(String), default=[], nullable=True) # use enum StyleEnum
