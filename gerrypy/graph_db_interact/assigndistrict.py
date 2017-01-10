"""Use the graph to assign districts to tracts."""
import networkx as nx
from gerrypy.models.mymodel import Tract


def assign_district(request, graph):
    """Assign a district ID to a single row in tract table."""
    for tract in nx.nodes(graph):
        tract_row = request.dbsession.query(Tract).get(tract.gid)
        tract_row.districtid = tract.districtid