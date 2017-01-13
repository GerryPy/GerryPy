import pytest
import transaction
from pyramid import testing
from gerrypy.models.mymodel import Tract, District, Edge, DistrictView
from gerrypy.models.meta import Base
from gerrypy.scripts.fish_scales import State, OccupiedDist
from gerrypy.graph_db_interact.assigndistrict import populate_district_table, assign_district
import sys
import os
import networkx as nx
from geoalchemy2 import Geometry
from gerrypy.views.default import build_JSON


@pytest.fixture(scope="session")
def configuration(request):
    """Set up a Configurator instance.
    This Configurator instance sets up a pointer to the location of the
        database.
    It also includes the models from your app's model package.
    Finally it tears everything down, including the in-memory SQLite database.
    This configuration will persist for the entire duration of your PyTest run.
    """
    config = testing.setUp(settings={
        'sqlalchemy.url': os.environ['SQL_URL_TEST']
    })
    config.include("gerrypy.models")
    config.include("gerrypy.routes")

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture(scope="function")
def db_session(configuration, request):
    """Create a session for interacting with the test database.
    This uses the dbsession_factory on the configurator instance to create a
    new database session. It binds that session to the available engine
    and returns a new session for every call of the dummy_request object.
    """
    SessionFactory = configuration.registry["dbsession_factory"]
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session):
    return testing.DummyRequest(dbsession=db_session)


@pytest.fixture
def filled_graph(dummy_request):
    """Import fill_graph as a fixture."""
    from gerrypy.scripts.fish_scales import fill_graph
    return fill_graph(dummy_request)


@pytest.fixture
def cleared_districts(db_session):
    """Set all districtIds to NULL in tract table."""
    rows = db_session.query(Tract).all()
    for row in rows:
        row.districtid = None


@pytest.fixture
def sample_state(dummy_request, filled_graph):
    """Create a sample state with some district data."""
    test_district1 = OccupiedDist('placeholder', filled_graph)
    test_district1.population = 500
    test_district1.area = 2500
    test_district1.districtID = 500
    test_district2 = OccupiedDist('placeholder', filled_graph)
    test_district2.population = 53043
    test_district2.area = 250420
    test_district2.districtID = 600
    test_district3 = OccupiedDist('placeholder', filled_graph)
    test_district3.population = 123
    test_district3.area = 456
    test_district3.districtID = 789
    test_state = State(dummy_request, 7)
    test_state.districts.extend([test_district1, test_district2, test_district3])
    return test_state


# ------DB Unit Tests--------

def test_database_has_tracts(db_session):
    """Test that database has contents."""
    assert db_session.query(Tract).count() == 1249


def test_database_has_edges(db_session):
    """Test that database has contents."""
    assert db_session.query(Edge).count() == 15948


def test_edit_districtid(db_session):
    """Test that editing district works correctly."""
    sample_row = db_session.query(Tract).first()
    sample_row.disrictid = 50
    assert sample_row.disrictid == 50


def test_empty_district_nums(dummy_request, cleared_districts):
    """Test that all districts have no district id before they're filled."""
    query = dummy_request.dbsession.query(Tract)
    no_d_id = query.filter(Tract.districtid == None).count()
    assert no_d_id == 1249


def test_empty_district_nums_after_fill(dummy_request, filled_graph):
    """Test that not all districts have no district id after they're filled."""
    query = dummy_request.dbsession.query(Tract)
    criteria = {
        'county': 1,
        'compactness': 1
    }
    state = State(dummy_request, 1)
    state.fill_state(dummy_request, criteria)
    no_d_id = query.filter(Tract.districtid == None).count()
    assert no_d_id < 1249


def test_assign_district_add_one_dist_id(dummy_request, filled_graph, cleared_districts):
    """Test that a district id is filled by assign_district."""
    nx.nodes(filled_graph)[0].districtid = 3
    assign_district(dummy_request, filled_graph)
    query = dummy_request.dbsession.query(Tract)
    no_d_id = query.filter(Tract.districtid == None).count()
    assert no_d_id == 1248


def test_assign_district_adds_mult_dist_ids(dummy_request, filled_graph, cleared_districts):
    """Test that multiple district ids are filled by assign_district."""
    nx.nodes(filled_graph)[0].districtid = 3
    nx.nodes(filled_graph)[1].districtid = 4
    assign_district(dummy_request, filled_graph)
    query = dummy_request.dbsession.query(Tract)
    no_d_id = query.filter(Tract.districtid == None).count()
    assert no_d_id == 1247


def test_assign_district_correct_dist_assigned(dummy_request, filled_graph):
    """Test that assign_district adds the correct district to the db."""
    tractid = nx.nodes(filled_graph)[0].gid
    nx.nodes(filled_graph)[0].districtid = 3
    assign_district(dummy_request, filled_graph)
    query = dummy_request.dbsession.query(Tract)
    test_tract = query.filter(Tract.gid == tractid).first()
    assert test_tract.districtid == 3


def test_insert_district_table(dummy_request):
    """Test that our code to truncate district table works."""
    test_row1 = District(districtid=456,
                         population=5000,
                         area=200)
    test_row2 = District(districtid=789,
                         population=5400,
                         area=400)
    current_length = dummy_request.dbsession.query(District).count()
    dummy_request.dbsession.add(test_row1)
    dummy_request.dbsession.add(test_row2)
    assert dummy_request.dbsession.query(District).count() == current_length + 2


def test_truncate_district_table(dummy_request):
    """Test that our code to truncate district table works."""
    test_row1 = District(districtid=789,
                         population=5000,
                         area=200)
    test_row2 = District(districtid=111,
                         population=5400,
                         area=400)
    dummy_request.dbsession.add(test_row1)
    dummy_request.dbsession.add(test_row2)
    dummy_request.dbsession.query(District).delete()
    assert dummy_request.dbsession.query(District).count() == 0


def test_populate_district_table(dummy_request, sample_state):
    """Test district is correct length after population."""
    populate_district_table(dummy_request, sample_state)
    query = dummy_request.dbsession.query(District)
    assert query.count() == 3


def test_populate_district_table_nonunique_id(dummy_request, sample_state):
    """Test populate district adds correct data."""
    populate_district_table(dummy_request, sample_state)
    query = dummy_request.dbsession.query(District).get(600)
    assert query.area == 250420

# =======View Unit Tests ================


# def test_build_json_returns_correct_data(dummy_request, cleared_districts):
#     """Test that build_json builds the proper json."""
#     tract1 = dummy_request.dbsession.query(Tract).get(1)
#     tract2 = dummy_request.dbsession.query(Tract).get(2)
#     tract1.districtid = 1000
#     tract2.districtid = 1000
#     import pdb; pdb.set_trace()
#     returned_json = build_JSON(dummy_request)['geometry']
#     geojson_db = dummy_request.dbsession.query(DistrictView.geom.ST_AsGeoJSON()).all()[0]
#     assert returned_json == geojson_db

# =======Functional Tests ================


@pytest.fixture()
def testapp():
    """Create an instance of our app for testing."""
    from pyramid.config import Configurator
    from webtest import TestApp

    def main(global_config, **settings):
        """Return a Pyramid WSGI application."""
        config = Configurator(settings=settings)
        config.include('pyramid_jinja2')
        config.include('gerrypy.models')
        config.include('gerrypy.routes')
        config.scan()
        return config.make_wsgi_app()
    app = main({}, **{"sqlalchemy.url": os.environ['SQL_URL_TEST']})
    SessionFactory = app.registry["dbsession_factory"]
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)
    return TestApp(app)


def test_home_page_has_content(testapp):
    """Test that home page has expected string."""
    response = testapp.get('/', status=200)
    html = response.html
    assert 'Let the machines' in str(html)


def test_home_page_has_title(testapp):
    """Test that home page has a title."""
    response = testapp.get('/', status=200)
    html = response.html
    assert 'GerryPy' in str(html.findAll("title")[0])


def test_map_page_has_content(testapp):
    """Test that map page has expected string."""
    response = testapp.get('/map', status=200)
    html = response.html
    assert 'Generate Districts' in str(html)


def test_map_page_has_title(testapp):
    """Test that map page has a title."""
    response = testapp.get('/map', status=200)
    html = response.html
    assert 'GerryPy' in str(html.findAll("title")[0])


def test_map_page_has_map(testapp):
    """Test that map page has map canvas."""
    response = testapp.get('/map', status=200)
    html = response.html
    assert html.find("div", {"id": "map"})


def test_map_page_loads_json(testapp):
    """Test that map page loads json after get request."""
    get_params = {'countyweight': 1, 'compactweight': 1}

    response = testapp.get('/map', get_params, status=200)
    assert 'map.data.loadGeoJson' in str(response)


def test_map_page_loads_correct_json(testapp):
    """Test that map page loads json after get request."""
    get_params = {'countyweight': 1, 'compactweight': 1}
    response = testapp.get('/map', get_params, status=200)
    json_url = response.html.find('script').attrs['data-json']
    json_response = testapp.get(json_url, status=200).text
    with open('gerrypy/views/geo.json', 'r') as the_file:
        our_json = the_file.read()
    assert our_json == json_response

