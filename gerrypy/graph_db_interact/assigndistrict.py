"""Use the graph to assign districts to tracts."""
import networkx as nx
from gerrypy.models.mymodel import Tract, District
from sqlalchemy import func
from sqlalchemy.sql import label
from geoalchemy2 import Geometry
from geoalchemy2.functions import ST_Union



def assign_district(request, graph):
    """Assign a district ID to a single row in tract table."""
    for tract in nx.nodes(graph):
        tract_row = request.dbsession.query(Tract).get(tract.gid)
        tract_row.districtid = tract.districtid


def populate_district_table(request, state):
    """Insert distrcts into district."""
    request.dbsession.query(District).delete()
    for district in state.districts:
        import pdb; pdb.set_trace()
        dist_geom = request.dbsession.query(func.ST_Union('geom').filter(Tract.districtid == district.districtID).group_by(Tract.districtid))[0][0]    
        new_district = District(id=district.districtID,
                                population=district.population,
                                area=district.area,
                                geom=dist_geom)
        request.dbsession.add(new_district)
