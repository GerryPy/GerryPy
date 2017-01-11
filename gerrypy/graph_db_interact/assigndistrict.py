"""Use the graph to assign districts to tracts."""
# import networkx as nx
from gerrypy.models.mymodel import Tract, District
# from gerrypy.scripts.fish_scales import State
# from sqlalchemy import func
# from sqlalchemy.sql import label
# from geoalchemy2.functions import ST_Union


def assign_district(request, state):
    """Assign a district ID to a single row in tract table."""
    for district in state.districts:
        for tract in district.nodes.nodes():
            tract_row = request.dbsession.query(Tract).get(tract.gid)
            tract_row.districtid = tract.districtid


def populate_district_table(request, state):
    """Insert distrcts into district."""
    request.dbsession.query(District).delete()
    for district in state.districts:
        new_district = District(districtid=district.districtID,
                                population=district.population,
                                area=district.area)
        request.dbsession.add(new_district)
    request.dbsession.execute('select * from update_district();')
