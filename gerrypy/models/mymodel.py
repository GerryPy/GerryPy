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


# This View uses on the fly calculations to agregate district data and shapes
class DistrictView(Base):
    """Model for each district built by the program."""

    __tablename__ = 'vwdistrict'
    districtid = Column(Integer, primary_key=True)
    area = Column(Float)
    population = Column(Integer)
    geom = Column(Geometry('MultiPolygon'))


# Tract table built from a Census shapefile using PostGIS
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


# The edges are calculated using the PostGIS function ST_Touches
# They represent tract borders, and become edges in the graph
class Edge(Base):
    """Edge model in the database."""

    __tablename__ = 'edge'
    edgeid = Column(Integer, primary_key=True)
    tract_source = Column(Integer)
    tract_target = Column(Integer)
