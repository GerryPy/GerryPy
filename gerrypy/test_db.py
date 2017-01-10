import pytest
import transaction
from pyramid import testing
from gerrypy.models.mymodel import Tract, District, Edge
from gerrypy.models.meta import Base
from gerrypy.graph_db_interact.assigndistrict import assign_district, populate_district_table
import sys
import os
import networkx as nx


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

# ------DB Tests--------


# def test_database_has_tracts(db_session):
#     """Test that database has contents."""
#     assert db_session.query(Tract).count() == 1249


# def test_database_has_edges(db_session):
#     """Test that database has contents."""
#     assert db_session.query(Edge).count() == 15948


# def test_edit_districtid(db_session):
#     """Test that editing district works correctly."""
#     sample_row = db_session.query(Tract).first()
#     sample_row.disrictid = 50
#     assert sample_row.disrictid == 50


# def test_empty_district_nums(dummy_request, filled_graph):
#     """Test that all districts have no district id before they're filled."""
#     query = dummy_request.dbsession.query(Tract)
#     no_d_id = query.filter(Tract.districtid == None).count()
#     assert no_d_id == 1249


# def test_assign_district_add_one_dist_id(dummy_request, filled_graph):
#     """Test that a district id is filled by assign_district."""
#     nx.nodes(filled_graph)[0].districtid = 3
#     assign_district(dummy_request, filled_graph)
#     query = dummy_request.dbsession.query(Tract)
#     no_d_id = query.filter(Tract.districtid == None).count()
#     assert no_d_id == 1248


# def test_assign_district_adds_mult_dist_ids(dummy_request, filled_graph):
#     """Test that multiple district ids are filled by assign_district."""
#     nx.nodes(filled_graph)[0].districtid = 3
#     nx.nodes(filled_graph)[1].districtid = 4
#     assign_district(dummy_request, filled_graph)
#     query = dummy_request.dbsession.query(Tract)
#     no_d_id = query.filter(Tract.districtid == None).count()
#     assert no_d_id == 1247


# def test_assign_district_correct_dist_assigned(dummy_request, filled_graph):
#     """Test that assign_district adds the correct district to the db."""
#     tractid = nx.nodes(filled_graph)[0].gid
#     nx.nodes(filled_graph)[0].districtid = 3
#     assign_district(dummy_request, filled_graph)
#     query = dummy_request.dbsession.query(Tract)
#     test_tract = query.filter(Tract.gid == tractid).first()
#     assert test_tract.districtid == 3


def test_insert_district_table(dummy_request):
    """Test that our code to truncate district table works."""
    test_row1 = District(id=1,
                         population=5000,
                         area=200)
    test_row2 = District(id=3,
                         population=5400,
                         area=400)
    dummy_request.dbsession.add(test_row1)
    dummy_request.dbsession.add(test_row2)
    assert dummy_request.dbsession.query(District).count() == 2


def test_truncate_district_table(dummy_request):
    """Test that our code to truncate district table works."""
    test_row1 = District(id=1,
                         population=5000,
                         area=200)
    test_row2 = District(id=3,
                         population=5400,
                         area=400)
    dummy_request.dbsession.add(test_row1)
    dummy_request.dbsession.add(test_row2)
    dummy_request.dbsession.query(District).delete()
    assert dummy_request.dbsession.query(District).count() == 0
