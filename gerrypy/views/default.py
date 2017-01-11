from pyramid.view import view_config
from gerrypy.scripts.fish_scales import State
from gerrypy.graph_db_interact.assigndistrict import assign_district, populate_district_table
import geoalchemy2


@view_config(route_name='home', renderer='../templates/home.jinja2')
def home_view(request):
    # state = State(request, 7)
    # state.fill_state()
    # assign_district(request, state)
    # populate_district_table(request, state)
    return {'css':'yes'}


@view_config(route_name='map', renderer='../templates/map.jinja2')
def map_view(request):
    return {}