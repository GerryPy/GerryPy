"""Define the models for the program."""

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Float
)

from .meta import Base


class District(Base):
    """Model for each district built by the program."""

    __tablename__ = 'districts'
    id = Column(Integer, primary_key=True)
    district_number = Column(Integer)
    area = Column(Float)
    population = Column(Integer)


Index('district_num', District.district_number, unique=True, mysql_length=255)
