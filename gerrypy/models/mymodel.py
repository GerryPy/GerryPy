"""Define the models for the program."""

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Float,
    Numeric
)

from geoalchemy2 import Geometry
from .meta import Base


class District(Base):
    """Model for each district built by the program."""

    __tablename__ = 'district'
    districtid = Column(Integer, primary_key=True)
    #district_number = Column(Integer)
    area = Column(Float)
    population = Column(Integer)
    geom = Column(Geometry('MultiPolygon'))


class DistrictView(Base):
    """Model for each district built by the program."""
    __tablename__ = 'vwdistrict'
    districtid = Column(Integer, primary_key=True)
    #district_number = Column(Integer)
    area = Column(Float)
    population = Column(Integer)
    geom = Column(Geometry('MultiPolygon'))


class Tract(Base):
    """Tract model in the db."""
    __tablename__ = 'colorado_tracts'
    gid = Column(Integer, primary_key=True)
    districtid = Column(Integer)
    shape_area = Column(Numeric)
    tract_pop = Column(Integer)
    geom = Column(Geometry('MultiPolygon'))
    isborder = Column(Integer)
    county = Column(Integer)


class Edge(Base):
    """Edge model in the database."""
    __tablename__ = 'edge'
    edgeid = Column(Integer, primary_key=True)
    tract_source = Column(Integer)
    tract_target = Column(Integer)



Index('district_num', District.districtid, unique=True, mysql_length=255)
