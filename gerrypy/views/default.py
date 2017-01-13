"""Handle view requests."""
from pyramid.view import view_config
from gerrypy.scripts.fish_scales import State
from gerrypy.models.mymodel import DistrictView


@view_config(route_name='home', renderer='../templates/home.jinja2')
def home_view(request):
    """Return css yes...for the home page."""
    return {'css': 'yes'}


@view_config(route_name='map', renderer='../templates/map.jinja2')
def map_view(request):
    """If form submitted, generate districts and return map with geojson."""
    if request.GET:
        criteria = {
            'county' : request.GET['countyweight'],
            'compactness' : request.GET['compactweight']
        }
        num_dst = 7
        state = State(request, num_dst)
        state.fill_state(request, criteria)
        with open('gerrypy/views/geo.json', 'w') as the_file:
            the_file.write(build_JSON(request))
        return {'geojson': 'ok'}
    return {}


@view_config(route_name='about', renderer='../templates/about.jinja2')
def about_view(request):
    """Return info about gerrypy creator extraordinaires."""
    with open("gerrypy/static/profiledescs/averydesc.txt") as fial:
        averydesc = fial.read()
    with open("gerrypy/static/profiledescs/forddesc.txt") as fial:
        forddesc = fial.read()
    with open("gerrypy/static/profiledescs/juliendesc.txt") as fial:
        juliendesc = fial.read()
    with open("gerrypy/static/profiledescs/patrickdesc.txt") as fial:
        patrickdesc = fial.read()
    with open("gerrypy/static/profiledescs/jordandesc.txt") as fial:
        jordandesc = fial.read()
    with open("gerrypy/static/gerrypydesc.txt") as fial:
        gerrypydesc = fial.read()
    return {
        "averydesc": averydesc,
        "forddesc": forddesc,
        "juliendesc": juliendesc,
        "patrickdesc": patrickdesc,
        "jordandesc": jordandesc,
        "gerrypydesc": gerrypydesc,
    }


def build_JSON(request):
    """Build JSON from the polygons in the database."""
    json_string = '{"type": "FeatureCollection","features": ['

    # query = request.dbsession.query(Tract.geom.ST_AsGeoJSON()).all()
    geojson_queries = request.dbsession.query(DistrictView.geom.ST_AsGeoJSON()).all()
    properties = request.dbsession.query(DistrictView).all()
    colors = ['blue', 'red', 'yellow', 'purple', 'orange', 'green', 'black']

    for idx, block in enumerate(properties):
        json_string += '{' + '"type": "Feature", "properties": '
        json_string += '{'
        json_string += '"id": {}, "area": {}, "population": {}, "color": "{}"'.format(str(block.districtid), str(block.area), str(block.population), str(colors[idx % 7])) + '}'
        json_string += ', "geometry": {}'.format(geojson_queries[idx][0]) + '}' + ','
    return json_string[:-1] + ']}'
