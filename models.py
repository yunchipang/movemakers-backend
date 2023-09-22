from sqlalchemy import Column, Integer, String
from sqlalchemy.types import ARRAY

from database import Base
from enums import Role, Style

class Dancer(Base):
    __tablename__ = "dancers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    instagram_handle = Column(String, unique=True, index=True)
    roles = Column(ARRAY(String), default=[], nullable=True) # use enum Role
    styles = Column(ARRAY(String), default=[], nullable=True) # use enum Style
