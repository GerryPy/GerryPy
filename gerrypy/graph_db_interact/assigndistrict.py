"""Use the graph to assign districts to tracts."""


def assign_district(request, graph):
    """Assign a district ID to a single row in tract table."""
    for tract in graph.nodes:
        tract_row = request.dbsession.query(Tract).get(tract.gid)
        tract_row.districtid = tract.districtid