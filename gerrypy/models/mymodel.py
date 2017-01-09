"""Define the models for the program."""

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Float,
    Numeric
)

from .meta import Base


class District(Base):
    """Model for each district built by the program."""

    __tablename__ = 'districts'
    id = Column(Integer, primary_key=True)
    district_number = Column(Integer)
    area = Column(Float)
    population = Column(Integer)


class Tract(Base):
    """Graph used to assign districts to tracts in the db."""
    __tablename__ == 'colorado_tracts'
    gid = Column(Integer, primary_key=True)
    districtid = Column(Integer)
    shape_area = Column(Numeric)
    tract_pop = Column(Integer)

    # def assign_distict(self, id):
    #     """Assign district to the tract."""
    #     self.districtid = id


Index('district_num', District.district_number, unique=True, mysql_length=255)
