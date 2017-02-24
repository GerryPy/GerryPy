"""Use the graph to assign districts to tracts."""
from gerrypy.models.mymodel import Tract


def assign_district(request, graph):
    """Assign district IDs to all of the tracts in the tract table."""
    for tract in graph.nodes():
        tract_row = request.dbsession.query(Tract).get(tract.gid)
        tract_row.districtid = tract.districtid
        request.dbsession.flush()
