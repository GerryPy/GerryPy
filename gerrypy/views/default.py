"""Handle view requests."""
from pyramid.view import view_config
from gerrypy.scripts.fish_scales import State
from gerrypy.models.mymodel import DistrictView


@view_config(route_name='home', renderer='../templates/home.jinja2')
def home_view(request):
    """Return the home page template."""
    return {}


@view_config(route_name='map', renderer='../templates/map.jinja2')
def map_view(request):
    """If form submitted, generate districts and build geojson api."""
    if request.GET:  # Unless 'Generate Districts' is clicked, there are no GET params.
        criteria = {
            'county': request.GET['countyweight'],
            'compactness': request.GET['compactweight']
        }
        num_dst = 7
        state = State(request, num_dst)
        state.fill_state(criteria)
        with open('gerrypy/static/geo.json', 'w') as the_file:  # Builds the API for GMaps to read.
            the_file.write(build_JSON(request))
        return {'geojson': 'ready'}
    return {}


@view_config(route_name='about', renderer='../templates/about.jinja2')
def about_view(request):
    """Return info about GerryPy creator extraordinaires."""
    with open("gerrypy/static/profiledescs/averydesc.txt") as the_file:
        averydesc = the_file.read()
    with open("gerrypy/static/profiledescs/forddesc.txt") as the_file:
        forddesc = the_file.read()
    with open("gerrypy/static/profiledescs/juliendesc.txt") as the_file:
        juliendesc = the_file.read()
    with open("gerrypy/static/profiledescs/patrickdesc.txt") as the_file:
        patrickdesc = the_file.read()
    with open("gerrypy/static/profiledescs/jordandesc.txt") as the_file:
        jordandesc = the_file.read()
    with open("gerrypy/static/gerrypydesc.txt") as the_file:
        gerrypydesc = the_file.read()
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
    geojson_queries = request.dbsession.query(DistrictView.geom.ST_AsGeoJSON()).all()
    properties = request.dbsession.query(DistrictView).all()
    colors = ['blue', 'red', 'yellow', 'purple', 'orange', 'green', 'black']

    json_string = '{"type": "FeatureCollection","features": ['
    for idx, block in enumerate(properties):
        json_string += '{' + '"type": "Feature", "properties": '
        json_string += '{'
        json_string += '"id": {}, "area": {}, "population": {}, "color": "{}"'.format(str(block.districtid), str(block.area), str(block.population), str(colors[idx % 7])) + '}'
        json_string += ', "geometry": {}'.format(geojson_queries[idx][0]) + '}' + ','
    return json_string[:-1] + ']}'
