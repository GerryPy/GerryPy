"""A class that contains a model for edges that link two tracts."""


from sqlalchemy import (
    Column,
    Integer,
)

from .meta import Base


class Edge(Base):
    """Model for edges between two tracts."""
    __tablename__ = 'edge'
    edgeid = Column(Integer, primary_key=True)
    tract_source = Column(Integer)
    tract_target = Column(Integer)
