"""A class that contains a model for a state's tracts."""


from sqlalchemy import (
    Column,
    Integer,
)

from .meta import Base


class Tract(Base):
    """Model for Tracts in a state."""
    __tablename__ = 'colorado_tracts'
    id = Column(Integer, primary_key=True)
    district_number = Column(Integer)
    population = Column(Integer)
