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


@pytest.fixture
def fill_colorado(dummy_request, filled_graph):
    """Build a state with a single district."""
    from gerrypy.scripts.fish_scales import State
    colorado = State(dummy_request, 1)
    colorado.build_district(colorado.population, 1, filled_graph)
    return colorado


# def test_fill_graph_from_db(filled_graph, dummy_request):
#     """Test that fill graph returns a graph with nodes that represent tracts."""
#     assert len(filled_graph.nodes()) == len(dummy_request.dbsession.query(Tract).all())


# def test_district_constructor():
#     """Test that district constructor creates properties for population, nodes, and perimeters."""
#     from gerrypy.scripts.fish_scales import OccupiedDist
#     dist = OccupiedDist(1)
#     assert (
#         dist.nodes.nodes() == [] and
#         dist.perimeter == [] and
#         dist.population == 0
#     )


# def test_unoc_constructor_nodes():
#     """Test that unoccupied district constructor creates properties for population, nodes, and perimeters."""
#     from gerrypy.scripts.fish_scales import UnoccupiedDist
#     unoc = UnoccupiedDist(None)
#     assert unoc.nodes.nodes() == []


# def test_unoc_constructor_perimeter():
#     """Test that unoccupied district constructor creates properties for population, nodes, and perimeters."""
#     from gerrypy.scripts.fish_scales import UnoccupiedDist
#     unoc = UnoccupiedDist(None)
#     assert unoc.perimeter == []


# def test_unoc_constructor_population():
#     """Test that unoccupied district constructor creates properties for population, nodes, and perimeters."""
#     from gerrypy.scripts.fish_scales import UnoccupiedDist
#     unoc = UnoccupiedDist(None)
#     assert unoc.population == 0


# def test_district_add_node(filled_graph):
#     """Test that district add_node method properly adds a node to nodes."""
#     from gerrypy.scripts.fish_scales import OccupiedDist
#     dist = OccupiedDist(1)
#     node_pop = 0
#     for node in filled_graph:
#         dist.add_node(node, filled_graph)
#         node_pop += node.tract_pop
#     assert dist.nodes.nodes().sort(key=lambda t: t.gid) == filled_graph.nodes().sort(key=lambda t: t.gid)


# def test_district_add_node_population(filled_graph):
#     """Test that district add_node method properly adds a node to nodes."""
#     from gerrypy.scripts.fish_scales import OccupiedDist
#     dist = OccupiedDist(1)
#     node_pop = 0
#     for node in filled_graph:
#         dist.add_node(node, filled_graph)
#         node_pop += node.tract_pop
#     assert dist.population == node_pop


# def test_district_add_node_perimeter(filled_graph):
#     """Test that district add_node method properly adds a node to nodes."""
#     from gerrypy.scripts.fish_scales import OccupiedDist
#     dist = OccupiedDist(1)
#     node_pop = 0
#     for node in filled_graph:
#         dist.add_node(node, filled_graph)
#         node_pop += node.tract_pop
#     assert dist.perimeter == []


# def test_unoc_add_node(filled_graph):
#     """Test that unoccupied district add_node method properly adds a node to nodes."""
#     from gerrypy.scripts.fish_scales import UnoccupiedDist
#     unoc = UnoccupiedDist(None)
#     node_pop = 0
#     filled_graph_perim = []
#     for node in filled_graph:
#         if filled_graph.neighbors(node):  # if node borders state
#             filled_graph_perim.append(node)
#     for node in filled_graph:
#         unoc.add_node(node, filled_graph)
#         node_pop += node.tract_pop
#     assert (
#         unoc.nodes.nodes().sort(key=lambda t: t.gid) == filled_graph.nodes().sort(key=lambda t: t.gid) and
#         unoc.population == node_pop
#         # unoc.population == node_pop and
#         # len(unoc.perimeter) == 36
#         # unoc.perimeter.sort() == filled_graph_perim.sort()
#     )


# def test_district_rem_node(filled_graph):
#     """Test that district rem_node method properly removes a node from nodes."""
#     from gerrypy.scripts.fish_scales import OccupiedDist
#     dist = OccupiedDist(1)
#     node_pop = 0
#     for node in filled_graph:
#         dist.add_node(node, filled_graph)
#         node_pop += node.tract_pop
#     removed = filled_graph.nodes()[0]
#     node_pop -= removed.tract_pop
#     dist.rem_node(removed, filled_graph)
#     assert len(dist.nodes.nodes()) == len(filled_graph.nodes()) - 1


# def test_district_rem_node_population(filled_graph):
#     """Test that district rem_node method properly removes a node from nodes."""
#     from gerrypy.scripts.fish_scales import OccupiedDist
#     dist = OccupiedDist(1)
#     node_pop = 0
#     for node in filled_graph:
#         dist.add_node(node, filled_graph)
#         node_pop += node.tract_pop
#     removed = filled_graph.nodes()[0]
#     node_pop -= removed.tract_pop
#     dist.rem_node(removed, filled_graph)
#     assert dist.population == node_pop


# def test_district_rem_node_perimeter(filled_graph):
#     """Test that district rem_node method properly removes a node from nodes."""
#     from gerrypy.scripts.fish_scales import OccupiedDist
#     dist = OccupiedDist(1)
#     node_pop = 0
#     for node in filled_graph:
#         dist.add_node(node, filled_graph)
#         node_pop += node.tract_pop
#     removed = filled_graph.nodes()[0]
#     node_pop -= removed.tract_pop
#     dist.rem_node(removed, filled_graph)
#     assert dist.perimeter == [removed]


# def test_unoc_rem_node(filled_graph):
#     """Test that unoccupied district rem_node method properly removes a node from nodes."""
#     from gerrypy.scripts.fish_scales import UnoccupiedDist
#     unoc = UnoccupiedDist(None)
#     node_pop = 0
#     filled_graph_perim = []
#     for node in filled_graph:
#         if filled_graph.neighbors(node):  # if node borders state
#             filled_graph_perim.append(node)
#     for node in filled_graph:
#         unoc.add_node(node, filled_graph)
#         node_pop += node.tract_pop
#     removed = filled_graph.nodes()[0]
#     node_pop -= removed.tract_pop
#     unoc.rem_node(removed, filled_graph)
#     assert (
#         len(unoc.nodes) == len(filled_graph.nodes()) - 1 and
#         unoc.population == node_pop
#         # unoc.population == node_pop and
#         # unoc.perimeter.sort() == filled_graph_perim.sort()
#     )


# def test_district_rem_nodes(filled_graph):
#     """Test that district rem_node method properly removes a node from nodes."""
#     from gerrypy.scripts.fish_scales import OccupiedDist
#     dist = OccupiedDist(1)
#     node_pop = 0
#     for node in filled_graph:
#         dist.add_node(node, filled_graph)
#         node_pop += node.tract_pop
#     for ind in range(len(filled_graph) - 1):
#         removed = filled_graph.nodes()[len(filled_graph) - ind - 1]
#         node_pop -= removed.tract_pop
#         dist.rem_node(removed, filled_graph)
#     assert dist.nodes.nodes() == [list(filled_graph)[0]]


# def test_district_rem_nodes_population(filled_graph):
#     """Test that district rem_node method properly removes a node from nodes."""
#     from gerrypy.scripts.fish_scales import OccupiedDist
#     dist = OccupiedDist(1)
#     node_pop = 0
#     for node in filled_graph:
#         dist.add_node(node, filled_graph)
#         node_pop += node.tract_pop
#     for ind in range(len(filled_graph) - 1):
#         removed = filled_graph.nodes()[len(filled_graph) - ind - 1]
#         node_pop -= removed.tract_pop
#         dist.rem_node(removed, filled_graph)
#     assert dist.population == node_pop


# def test_district_rem_nodes_perimeter(filled_graph):
#     """Test that district rem_node method properly removes a node from nodes."""
#     from gerrypy.scripts.fish_scales import OccupiedDist
#     dist = OccupiedDist(1)
#     node_pop = 0
#     for node in filled_graph:
#         dist.add_node(node, filled_graph)
#         node_pop += node.tract_pop
#     for ind in range(len(filled_graph) - 1):
#         removed = filled_graph.nodes()[len(filled_graph) - ind - 1]
#         node_pop -= removed.tract_pop
#         dist.rem_node(removed, filled_graph)
#     assert dist.perimeter.sort(key=lambda tract: tract.gid) == filled_graph.neighbors(filled_graph.nodes()[0]).sort(key=lambda tract: tract.gid)


# def test_unoc_rem_nodes(filled_graph):
#     """Test that unoccupied district rem_node method properly removes a node from nodes."""
#     from gerrypy.scripts.fish_scales import UnoccupiedDist
#     unoc = UnoccupiedDist(None)
#     node_pop = 0
#     filled_graph_perim = []
#     for node in filled_graph:
#         if filled_graph.neighbors(node):  # if node borders state
#             filled_graph_perim.append(node)
#     for node in filled_graph:
#         unoc.add_node(node, filled_graph)
#         node_pop += node.tract_pop
#     for ind in range(len(filled_graph) - 1):
#         removed = filled_graph.nodes()[len(filled_graph) - ind - 1]
#         node_pop -= removed.tract_pop
#         unoc.rem_node(removed, filled_graph)
#     assert (
#         unoc.nodes.nodes() == [list(filled_graph)[0]] and
#         unoc.population == node_pop
#         # unoc.population == node_pop and
#         # unoc.perimeter.sort() == filled_graph_perim.sort()
#     )


# def test_state_unoccupied_length_for_colorado(dummy_request):
#     """Test that colorado State object builds one unoccupied district."""
#     from gerrypy.scripts.fish_scales import State, TRACTGRAPH
#     state = State(dummy_request, 7)
#     assert len(state.unoccupied) == 1


# def test_state_unoccupied_district_has_all_tracts(dummy_request):
#     """Test that the number of tracts in unoccupied district
#     matches the number of rows in the database."""
#     from gerrypy.scripts.fish_scales import State, TRACTGRAPH
#     state = State(dummy_request, 7)
#     nodes = state.unoccupied[0].nodes
#     queries = dummy_request.dbsession.query(Tract).all()
#     assert len(nodes) == len(queries)


# # def test_state_unoccupied_district_has_no_perimeter(dummy_request):
# #     """Test that the perimeter of the unoccupied district is empty."""
# #     from gerrypy.scripts.fish_scales import State, TRACTGRAPH
# #     state = State(dummy_request, 7)
# #     assert state.unoccupied[0].perimeter == []


# def test_state_population(dummy_request):
#     """Test that the population of the state is equal
#     to the sum of the tracts population in the database."""
#     from gerrypy.scripts.fish_scales import State, TRACTGRAPH
#     from sqlalchemy import func
#     state = State(dummy_request, 7)
#     pop = dummy_request.dbsession.query(func.sum(Tract.tract_pop)).scalar()
#     assert state.population == pop


# def test_state_districts(dummy_request):
#     """Test that districts property of an instance of State() is initialized to an empty list."""
#     from gerrypy.scripts.fish_scales import State, TRACTGRAPH
#     state = State(dummy_request, 7)
#     assert state.districts == []


def test_state_build_district(fill_colorado):
    """Test that tracts are added to districts."""
    assert fill_colorado.districts


def test_state_build_district_unoccupied(fill_colorado):
    """Test that filling the whole state with one district leaves no unoccupied tracts."""
    assert len(fill_colorado.districts[0].nodes.nodes()) > 0


def test_state_build_district_population(fill_colorado):
    """Test that district pop == state pop when there is one district in the state."""
    total_pop = fill_colorado.districts[0].population + fill_colorado.unoccupied[0].population
    assert fill_colorado.population == total_pop


def test_state_build_district_area(fill_colorado):
    """Test that district area == state area when there is one district in the state."""
    assert fill_colorado.area == fill_colorado.districts[0].area


def test_state_build_district_perimiter(fill_colorado):
    """Test that district perimiter == state perimiter when there is one district in the state."""
    assertion = True
    for tract in fill_colorado.districts[0].perimeter:
        if tract in fill_colorado.districts[0].nodes.nodes():
            assertion = False
    assert assertion


def test_swap_returns_correct_unoc_dist(dummy_request, filled_graph):
    """Test swap from unoc to oc returns the correct unoc district."""
    from gerrypy.scripts.fish_scales import State, OccupiedDist
    state = State(dummy_request, 2)
    node = filled_graph.nodes()[0]
    dst = OccupiedDist(1)
    state.unoccupied[0].perimeter.append(node)
    state.unoccupied[0].rem_node(node, filled_graph)
    dst.add_node(node, filled_graph)
    neighbors = filled_graph.neighbors(node)
    assert state.swap(dst, neighbors[0], filled_graph) is state.unoccupied[0]
    assert filled_graph.neighbors(node).sort(key=lambda tract: tract.gid) == state.unoccupied[0].perimeter.sort(key=lambda tract: tract.gid)

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
#     dist = OccupiedDist()
#     for node in sample_state:
#         dist.add_node(node)
#     assert (
#         dist.nodes == sample_state and
#         dist.perimeter == [] and
#         dist.population == 10
#     )
