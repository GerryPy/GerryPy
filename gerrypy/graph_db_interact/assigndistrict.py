"""Use the graph to assign districts to tracts."""
import networkx as nx
from gerrypy.models.mymodel import Tract, District
from sqlalchemy import func
from sqlalchemy.sql import label
import geoalchemy2.functions


def assign_district(request, graph):
    """Assign a district ID to a single row in tract table."""
    for tract in nx.nodes(graph):
        tract_row = request.dbsession.query(Tract).get(tract.gid)
        tract_row.districtid = tract.districtid


def populate_district_table(request, state):
    """Insert distrcts into district."""
    request.dbsession.query(District).delete()
    # geoms = request.dbsession.query(Tract.districtid,
    #                                 ST_Union(Tract.geom).label('geom').group_by(Tract.district))
    for district in state.districts:
        geom = request.dbsession.query(
            Tract.districtid,
            ST_Union(Tract.districtid).label('districtid')
            ).filter(Tract.districtid == district.districtID
            ).group_by(Tract.districtid
            ).all()
        import pdb; pdb.set_trace()
        new_district = District(id=district.districtID,
                                population=district.population,
                                area=district.area,
                                geom=geom)
        request.dbsession.add(new_district)
