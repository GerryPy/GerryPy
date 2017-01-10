"""Use the graph to assign districts to tracts."""
import networkx as nx
from gerrypy.models.mymodel import Tract, District


def assign_district(request, graph):
    """Assign a district ID to a single row in tract table."""
    for tract in nx.nodes(graph):
        tract_row = request.dbsession.query(Tract).get(tract.gid)
        tract_row.districtid = tract.districtid


def populate_district_table(request, state):
    """Insert distrcts into district."""
    request.dbsession.query(District).delete()
    for district in state.districts:
        # districtid =  district.districtid
        # population = district.population
        # area = district.shape_area
        district = District(id=district.districtid,
                            population=district.population,
                            area=district.shape_area)
        request.dbsession.add(district)