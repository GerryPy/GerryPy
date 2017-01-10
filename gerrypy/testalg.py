"""Test algorithm."""

import pytest
import os
from pyramid import testing
from gerrypy.models.mymodel import Tract, District, Edge
from gerrypy.models.meta import Base
from gerrypy.test_db import db_session, configuration


# @pytest.fixture(scope="session")
# def configuration(request):
#     """Set up a Configurator instance.
#     This Configurator instance sets up a pointer to the location of the
#         database.
#     It also includes the models from your app's model package.
#     Finally it tears everything down, including the in-memory SQLite database.
#     This configuration will persist for the entire duration of your PyTest run.
#     """
#     config = testing.setUp(settings={
#         'sqlalchemy.url': os.environ['SQL_URL']  # user testing database url
#     })
#     config.include("gerrypy.models")
#     config.include("gerrypy.routes")

#     def teardown():
#         testing.tearDown()

#     request.addfinalizer(teardown)
#     return config


# @pytest.fixture(scope="function")
# def db_session(configuration, request):
#     """Create a session for interacting with the test database.
#     This uses the dbsession_factory on the configurator instance to create a
#     new database session. It binds that session to the available engine
#     and returns a new session for every call of the dummy_request object.
#     """
#     SessionFactory = configuration.registry["dbsession_factory"]
#     session = SessionFactory()
#     engine = session.bind
#     Base.metadata.create_all(engine)

#     def teardown():
#         session.transaction.rollback()

#     request.addfinalizer(teardown)
#     return session


@pytest.fixture
def dummy_request(db_session):
    return testing.DummyRequest(dbsession=db_session)


@pytest.fixture
def filled_graph(dummy_request):
    """Import fill_graph as a fixture."""
    from gerrypy.scripts.fish_scales import fill_graph
    return fill_graph(dummy_request)


def test_fill_graph_from_db(filled_graph, dummy_request):
    """Test that fill graph returns a graph with nodes that represent tracts."""
    assert len(filled_graph.nodes()) == len(dummy_request.dbsession.query(Tract).all())


def test_unoccupied_length_for_colorado(dummy_request):
    """Test that colorado State object build one unoccupied district."""
    from gerrypy.scripts.fish_scales import State, TRACTGRAPH
    state = State(dummy_request, 7)
    assert len(state.unoccupied) == 1


def test_unoccupied_district_has_all_tracts(dummy_request):
    from gerrypy.scripts.fish_scales import State, TRACTGRAPH
    state = State(dummy_request, 7)
    nodes = state.unoccupied[0].nodes
    queries = dummy_request.dbsession.query(Tract).all()
    assert len(nodes) == len(queries)



# Algorithm tests


# NODES = [
#     [123456, None],
#     [200000, []],
#     [200000, ["data"]],
# ]


# NEIGHBORS = [
#     [],
#     [NODES[0]],
#     [NODES[0], NODES[1]]
# ]


# BAD_POP = [
#     [0, [], []],
#     [-123456, [], []],
# ]


# BAD_NEIGH = [
#     [100000, None, ["data"]],
#     [100000, [1, 2, 3], ["data"]],
#     [100000, ["four", "five", "six"], ["data"]],
# ]


# NODE_LST = [
#     [[], [], 0],
#     [[Node(1, ["data"])], [], 1],
#     [[Node(1, ["data"]), Node(10, ["more data"])], [], 11],
#     [[Node(1, ["data"]), Node(10, None)], [NEIGHBORS[0]], 11],
#     [[NEIGHBORS[0], NODES[2]], [NEIGHBORS[1]], 200001],
#     [[Node(1, ["data"]), NODES[2]], [NEIGHBORS[0], NEIGHBORS[1]], 2]
# ]


# BAD_NODES = [None, object, "string", 42, [], {}, [Node(1, None)]]


# @pytest.fixture
# def sample_state():
#     """Creates a list of nodes that are connected by borders like tracts in a state."""
#     nodes = [
#         Node(100, ["node 1"]),
#         Node(100, ["node 2"]),
#         Node(100, ["node 3"]),
#         Node(100, ["node 4"]),
#         Node(100, ["node 5"])
#     ]
#     nodes[0].add_neighbors([nodes[1], nodes[2], nodes[3], nodes[4]])
#     nodes[1].add_neighbors([nodes[4], nodes[2]])
#     nodes[2].add_neighbors([nodes[1], nodes[3]])
#     nodes[3].add_neighbors([nodes[2], nodes[4]])
#     nodes[4].add_neighbors([nodes[3], nodes[1]])
#     return nodes


# @pytest.mark.parametrize("pop, data", NODES)
# def test_node_constructor(pop, data):
#     """Tests that node constructor can contain population as a property."""
#     node = Node(pop, data)
#     assert (
#         node.population == pop and
#         node.data == data
#     )


# @pytest.mark.parametrize("pop, data", BAD_POP)
# def test_node_population_error(pop, data):
#     """Tests that node constructor raises an error when given a negative population."""
#     with pytest.raises(ValueError):
#         Node(pop, data)


# @pytest.mark.parametrize("pop, neigh, data", NEIGHBORS)
# def test_node_neighbors(pop, neigh, data):
#     """Tests that add_neighbors method of Node object adds a list of neighboring nodes to self."""
#     node = Node(pop, data)
#     node.add_neighbors(neigh)
#     assert node.neighbors == neigh


# @pytest.mark.parametrize("pop, neigh, data", BAD_NEIGH)
# def test_node_neighbors_error(pop, neigh, data):
#     """Tests that node constructor raises an error when given neighbors that are not node."""
#     node = Node(pop, data)
#     with pytest.raises(ValueError):
#         node.add_neighbors(neigh)


# def test_district_constructor():
#     """Tests that district constructor creates properties for population, nodes, and perimeters."""
#     from gerrypy.scripts.fish_scales import District
#     dist = District()
#     assert (
#         dist.nodes == [] and
#         dist.perimeter == [] and
#         dist.population == 0
#     )


# @pytest.mark.parametrize("node_lst, peri_lst, pop", NODE_LST)
# def test_district_add_node(node_lst, peri_lst, pop):
#     """Tests that district add_node method properly adds a node to nodes."""
#     from gerrypy.scripts.fish_scales import District
#     dist = District()
#     for node in node_lst:
#         dist.add_node(node)
#     assert (
#         dist.nodes == node_lst and
#         dist.perimeter == peri_lst and
#         dist.population == pop
#     )


# @pytest.mark.parametrize("bad_node", BAD_NODES)
# def test_district_add_node_error(bad_node):
#     """Tests that district add_node method raises an error when a non-node object is put into it."""
#     from gerrypy.scripts.fish_scales import District
#     dist = District()
#     with pytest.raises(ValueError):
#         dist.add_node(bad_node)


# def test_district_rem_node(sample_state):
#     """Tests that district rem_node properly removes a node from nodes."""
#     from gerrypy.scripts.fish_scales import District
#     dist = District()
#     for node in sample_state:
#         dist.add_node(node)
#     assert (
#         dist.nodes == sample_state and
#         dist.perimeter == [] and
#         dist.population == 10
#     )
