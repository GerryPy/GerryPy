"""Use the graph to assign districts to tracts."""
from gerrypy.models.mymodel import Tract, District


def assign_district(request, graph):
    """Assign a district ID to a single row in tract table."""
    # request.dbsession.execute('select * from reset_district();')
    for tract in graph.nodes():
        tract_row = request.dbsession.query(Tract).get(tract.gid)
        tract_row.districtid = tract.districtid
        request.dbsession.flush()


def populate_district_table(request, state):
    """Insert distrcts into district."""
    request.dbsession.query(District).delete()
    for district in state.districts:
        new_district = District(districtid=district.districtID,
                                population=district.population,
                                area=district.area)
        request.dbsession.add(new_district)
    request.dbsession.execute('select * from update_district();')
