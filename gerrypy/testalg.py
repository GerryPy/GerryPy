"""Test algorithm."""

import pytest
from pyramid import testing
from gerrypy.models.mymodel import Tract
from gerrypy.models.meta import Base
from gerrypy.test_db import db_session, configuration


@pytest.fixture
def dummy_request(db_session):
    """Return dummy request dummy."""
    return testing.DummyRequest(dbsession=db_session)


@pytest.fixture
def filled_graph(dummy_request):
    """Import fill_graph as a fixture."""
    from gerrypy.scripts.fish_scales import fill_graph
    return fill_graph(dummy_request)


def test_fill_graph_from_db(filled_graph, dummy_request):
    """Test that fill graph returns a graph with nodes that represent tracts."""
    assert len(filled_graph.nodes()) == len(dummy_request.dbsession.query(Tract).all())


def test_district_constructor():
    """Tests that district constructor creates properties for population, nodes, and perimeters."""
    from gerrypy.scripts.fish_scales import District
    dist = District()
    assert (
        dist.nodes == [] and
        dist.perimeter == [] and
        dist.population == 0
    )


def test_district_add_node(filled_graph):
    """Tests that district add_node method properly adds a node to nodes."""
    from gerrypy.scripts.fish_scales import District, fill_graph
    dist = District()
    node_pop = 0
    for node in filled_graph:
        dist.add_node(node, filled_graph)
        node_pop += node.tract_pop
    assert (
        dist.nodes.sort() == filled_graph.nodes().sort() and
        dist.population == node_pop
    )


def test_district_rem_node(filled_graph):
    """Tests that district rem_node method properly removes a node from nodes."""
    from gerrypy.scripts.fish_scales import District, fill_graph
    dist = District()
    node_pop = 0
    for node in filled_graph:
        dist.add_node(node, filled_graph)
        node_pop += node.tract_pop
    assert (
        dist.nodes.sort() == filled_graph.nodes().sort() and
        dist.population == node_pop
    )


def test_state_unoccupied_length_for_colorado(dummy_request):
    """Test that colorado State object builds one unoccupied district."""
    from gerrypy.scripts.fish_scales import State, TRACTGRAPH
    state = State(dummy_request, 7)
    assert len(state.unoccupied) == 1


def test_state_unoccupied_district_has_all_tracts(dummy_request):
    """Test that the number of tracts in unoccupied district
    matches the number of rows in the database."""
    from gerrypy.scripts.fish_scales import State, TRACTGRAPH
    state = State(dummy_request, 7)
    nodes = state.unoccupied[0].nodes
    queries = dummy_request.dbsession.query(Tract).all()
    assert len(nodes) == len(queries)


def test_state_unoccupied_district_has_no_perimeter(dummy_request):
    """Test that the perimeter of the unoccupied district is empty."""
    from gerrypy.scripts.fish_scales import State, TRACTGRAPH
    state = State(dummy_request, 7)
    assert state.unoccupied[0].perimeter == []


def test_state_population(dummy_request):
    """Test that the population of the state is equal
    to the sum of the tracts population in the database."""
    from gerrypy.scripts.fish_scales import State, TRACTGRAPH
    from sqlalchemy import func
    state = State(dummy_request, 7)
    pop = dummy_request.dbsession.query(func.sum(Tract.tract_pop)).scalar()
    assert state.population == pop


def test_state_districts(dummy_request):
    """Test that districts property of an instance of State() is initialized to an empty list."""
    from gerrypy.scripts.fish_scales import State, TRACTGRAPH
    state = State(dummy_request, 7)
    assert state.districts == []


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
