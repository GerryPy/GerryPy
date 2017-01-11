from pyramid.view import view_config
from gerrypy.scripts.fish_scales import State
from gerrypy.graph_db_interact.assigndistrict import assign_district, populate_district_table
import geoalchemy2
from gerrypy.models.mymodel import Tract, District

@view_config(route_name='home', renderer='../templates/home.jinja2')
def home_view(request):
    # state = State(request, 7)
    # state.fill_state()
    # assign_district(request, state)
    # populate_district_table(request, state)
    return {'css': 'yes'}


@view_config(route_name='map', renderer='../templates/map.jinja2')
def map_view(request):
    if request.GET:
        # Do all the stuff
        num_dst = 7
        # state = State(request, num_dst)
        # state.fill_state()
        # assign_district(request, state)
        # populate_district_table(request, state)
        import pdb; pdb.set_trace()

        json = build_JSON(request)
        for row in query:
            row.geom

        return {'geojson': 'https://storage.googleapis.com/mapsdevsite/json/google.json'}
    return {}


JSON_TEMPLATE =
    {
      "type": "Feature",
      "properties": {
        "id": {},
        "area": {},
        "population": {},
        "color": {},
        "ascii": "71"
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [123.61, -22.14], [122.38, -21.73], [121.06, -21.69], [119.66, -22.22], [119.00, -23.40],
            [118.65, -24.76], [118.43, -26.07], [118.78, -27.56], [119.22, -28.57], [120.23, -29.49],
            [121.77, -29.87], [123.57, -29.64], [124.45, -29.03], [124.71, -27.95], [124.80, -26.70],
            [124.80, -25.60], [123.61, -25.64], [122.56, -25.64], [121.72, -25.72], [121.81, -26.62],
            [121.86, -26.98], [122.60, -26.90], [123.57, -27.05], [123.57, -27.68], [123.35, -28.18],
            [122.51, -28.38], [121.77, -28.26], [121.02, -27.91], [120.49, -27.21], [120.14, -26.50],
            [120.10, -25.64], [120.27, -24.52], [120.67, -23.68], [121.72, -23.32], [122.43, -23.48],
            [123.04, -24.04], [124.54, -24.28], [124.58, -23.20], [123.61, -22.14]
          ]
        ]
      }
    },


def build_JSON(request):
    """Build JSON from the polygons in the database."""
    json_string = '{"type": "FeatureCollection","features": ['

    # query = request.dbsession.query(Tract.geom.ST_AsGeoJSON()).all()
    query = request.dbsession.query(Tract).all()


        {
      "type": "Feature",
      "properties": {
        "id": {},
        "area": {},
        "population": {},
        "color": {},
        "ascii": "71"
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [123.61, -22.14], [122.38, -21.73], [121.06, -21.69], [119.66, -22.22], [119.00, -23.40],
            [118.65, -24.76], [118.43, -26.07], [118.78, -27.56], [119.22, -28.57], [120.23, -29.49],
            [121.77, -29.87], [123.57, -29.64], [124.45, -29.03], [124.71, -27.95], [124.80, -26.70],
            [124.80, -25.60], [123.61, -25.64], [122.56, -25.64], [121.72, -25.72], [121.81, -26.62],
            [121.86, -26.98], [122.60, -26.90], [123.57, -27.05], [123.57, -27.68], [123.35, -28.18],
            [122.51, -28.38], [121.77, -28.26], [121.02, -27.91], [120.49, -27.21], [120.14, -26.50],
            [120.10, -25.64], [120.27, -24.52], [120.67, -23.68], [121.72, -23.32], [122.43, -23.48],
            [123.04, -24.04], [124.54, -24.28], [124.58, -23.20], [123.61, -22.14]
          ]
        ]
      }
    },