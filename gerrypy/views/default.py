from pyramid.view import view_config


@view_config(route_name='home', renderer='../templates/home.jinja2')
def home_view(request):
    return {'css':'yes'}


@view_config(route_name='map', renderer='../templates/map.jinja2')
def map_view(request):
    return {}