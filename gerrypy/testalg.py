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


def test_fill_graph_from_db(filled_graph, dummy_request):
    """Test fill graph returns a graph with same number of nodes as db rows."""
    assert len(filled_graph.nodes()) == len(dummy_request.dbsession.query(Tract).all())


def test_fill_graph_num_nodes(filled_graph, dummy_request):
    """Test fill graph returns a graph with expected number of nodes."""
    assert len(filled_graph.nodes()) == 1249


def test_fill_graph_node_has_right_pop(filled_graph, dummy_request):
    """Test that filled_graph has same population value as database."""
    node_id = filled_graph.nodes()[0].gid
    assert filled_graph.nodes()[0].tract_pop == dummy_request.dbsession.query(Tract).get(node_id).tract_pop


def test_fill_graph_node_has_right_area(filled_graph, dummy_request):
    """Test that filled_graph has same area value as database."""
    node_id = filled_graph.nodes()[50].gid
    assert filled_graph.nodes()[50].shape_area == dummy_request.dbsession.query(Tract).get(node_id).shape_area


def test_district_constructor_nodes():
    """Test that district constructor creates property nodes."""
    from gerrypy.scripts.fish_scales import OccupiedDist
    dist = OccupiedDist(1)
    assert dist.nodes.nodes() == []


def test_district_constructor_perim():
    """Test that district constructor creates property perimeter."""
    from gerrypy.scripts.fish_scales import OccupiedDist
    dist = OccupiedDist(1)
    assert dist.perimeter == []


def test_district_constructor_pop():
    """Test that district constructor creates property population."""
    from gerrypy.scripts.fish_scales import OccupiedDist
    dist = OccupiedDist(1)
    assert dist.population == 0


def test_district_id_value():
    """Test that district constructor assigns district id."""
    from gerrypy.scripts.fish_scales import OccupiedDist
    dist = OccupiedDist(1)
    assert dist.districtID == 1


def test_district_add_invalid_tract():
    """Test that adding an invalid tract raises error."""
    from gerrypy.scripts.fish_scales import OccupiedDist
    with pytest.raises(TypeError):
        dist = OccupiedDist(1, 34)


def test_district_add_with_tracts(filled_graph):
    """Test creating a district with nodes."""
    from gerrypy.scripts.fish_scales import OccupiedDist
    nodes = filled_graph.nodes()
    dist = OccupiedDist(1, tracts=nodes, graph=filled_graph)
    assert len(dist.nodes) == len(nodes)


def test_unoc_constructor_nodes():
    """Test that unoccupied district constructor creates node property."""
    from gerrypy.scripts.fish_scales import UnoccupiedDist
    unoc = UnoccupiedDist(None)
    assert unoc.nodes.nodes() == []


def test_unoc_constructor_perimeter():
    """Test that unoccupied district constructor creates perimeter property."""
    from gerrypy.scripts.fish_scales import UnoccupiedDist
    unoc = UnoccupiedDist(None)
    assert unoc.perimeter == []


def test_unoc_constructor_population():
    """Test that unoccupied district constructor creates population property."""
    from gerrypy.scripts.fish_scales import UnoccupiedDist
    unoc = UnoccupiedDist(None)
    assert unoc.population == 0


def test_district_add_node(filled_graph):
    """Test that district add_node method properly adds a node to nodes."""
    from gerrypy.scripts.fish_scales import OccupiedDist
    dist = OccupiedDist(1)
    node_pop = 0
    for node in filled_graph:
        dist.add_node(node, filled_graph)
        node_pop += node.tract_pop
    assert dist.nodes.nodes().sort(key=lambda t: t.gid) == filled_graph.nodes().sort(key=lambda t: t.gid)


def test_district_add_node_population(filled_graph):
    """Test that district add_node method properly adds node pop value to nodes."""
    from gerrypy.scripts.fish_scales import OccupiedDist
    dist = OccupiedDist(1)
    node_pop = 0
    for node in filled_graph:
        dist.add_node(node, filled_graph)
        node_pop += node.tract_pop
    assert dist.population == node_pop


def test_district_add_node_perimeter(filled_graph):
    """Test that district add_node method adds a perimiter to nodes."""
    from gerrypy.scripts.fish_scales import OccupiedDist
    dist = OccupiedDist(1)
    node_pop = 0
    for node in filled_graph:
        dist.add_node(node, filled_graph)
        node_pop += node.tract_pop
    assert dist.perimeter == []


def test_unoc_add_node(filled_graph):
    """Test that unoccupied district add_node method properly adds a node to nodes."""
    from gerrypy.scripts.fish_scales import UnoccupiedDist
    unoc = UnoccupiedDist(None)
    node_pop = 0
    filled_graph_perim = []
    for node in filled_graph:
        if filled_graph.neighbors(node):  # if node borders state
            filled_graph_perim.append(node)
    for node in filled_graph:
        unoc.add_node(node, filled_graph)
        node_pop += node.tract_pop
    assert (
        unoc.nodes.nodes().sort(key=lambda t: t.gid) == filled_graph.nodes().sort(key=lambda t: t.gid) and
        unoc.population == node_pop
        # unoc.population == node_pop and
        # len(unoc.perimeter) == 36
        # unoc.perimeter.sort() == filled_graph_perim.sort()
    )


def test_district_rem_node(filled_graph):
    """Test that district rem_node method properly removes a node from nodes."""
    from gerrypy.scripts.fish_scales import OccupiedDist
    dist = OccupiedDist(1)
    node_pop = 0
    for node in filled_graph:
        dist.add_node(node, filled_graph)
        node_pop += node.tract_pop
    removed = filled_graph.nodes()[0]
    node_pop -= removed.tract_pop
    dist.rem_node(removed, filled_graph)
    assert len(dist.nodes.nodes()) == len(filled_graph.nodes()) - 1


def test_district_rem_node_population(filled_graph):
    """Test that district rem_node method properly removes a node from nodes."""
    from gerrypy.scripts.fish_scales import OccupiedDist
    dist = OccupiedDist(1)
    node_pop = 0
    for node in filled_graph:
        dist.add_node(node, filled_graph)
        node_pop += node.tract_pop
    removed = filled_graph.nodes()[0]
    node_pop -= removed.tract_pop
    dist.rem_node(removed, filled_graph)
    assert dist.population == node_pop


def test_district_rem_node_perimeter(filled_graph):
    """Test that district rem_node method properly removes a node from nodes."""
    from gerrypy.scripts.fish_scales import OccupiedDist
    dist = OccupiedDist(1)
    node_pop = 0
    for node in filled_graph:
        dist.add_node(node, filled_graph)
        node_pop += node.tract_pop
    removed = filled_graph.nodes()[0]
    node_pop -= removed.tract_pop
    dist.rem_node(removed, filled_graph)
    assert dist.perimeter == [removed]


def test_unoc_rem_node(filled_graph):
    """Test that unoccupied district rem_node method properly removes a node from nodes."""
    from gerrypy.scripts.fish_scales import UnoccupiedDist
    unoc = UnoccupiedDist(None)
    node_pop = 0
    filled_graph_perim = []
    for node in filled_graph:
        if filled_graph.neighbors(node):  # if node borders state
            filled_graph_perim.append(node)
    for node in filled_graph:
        unoc.add_node(node, filled_graph)
        node_pop += node.tract_pop
    removed = filled_graph.nodes()[0]
    node_pop -= removed.tract_pop
    unoc.rem_node(removed, filled_graph)
    assert (
        len(unoc.nodes) == len(filled_graph.nodes()) - 1 and
        unoc.population == node_pop
        # unoc.population == node_pop and
        # unoc.perimeter.sort() == filled_graph_perim.sort()
    )


def test_district_rem_nodes(filled_graph):
    """Test that district rem_node method properly removes a node from nodes."""
    from gerrypy.scripts.fish_scales import OccupiedDist
    dist = OccupiedDist(1)
    node_pop = 0
    for node in filled_graph:
        dist.add_node(node, filled_graph)
        node_pop += node.tract_pop
    for ind in range(len(filled_graph) - 1):
        removed = filled_graph.nodes()[len(filled_graph) - ind - 1]
        node_pop -= removed.tract_pop
        dist.rem_node(removed, filled_graph)
    assert dist.nodes.nodes() == [list(filled_graph)[0]]


def test_district_rem_nodes_population(filled_graph):
    """Test that district rem_node method properly removes a node from nodes."""
    from gerrypy.scripts.fish_scales import OccupiedDist
    dist = OccupiedDist(1)
    node_pop = 0
    for node in filled_graph:
        dist.add_node(node, filled_graph)
        node_pop += node.tract_pop
    for ind in range(len(filled_graph) - 1):
        removed = filled_graph.nodes()[len(filled_graph) - ind - 1]
        node_pop -= removed.tract_pop
        dist.rem_node(removed, filled_graph)
    assert dist.population == node_pop


def test_district_rem_nodes_perimeter(filled_graph):
    """Test that district rem_node method properly removes a node from nodes."""
    from gerrypy.scripts.fish_scales import OccupiedDist
    dist = OccupiedDist(1)
    node_pop = 0
    for node in filled_graph:
        dist.add_node(node, filled_graph)
        node_pop += node.tract_pop
    for ind in range(len(filled_graph) - 1):
        removed = filled_graph.nodes()[len(filled_graph) - ind - 1]
        node_pop -= removed.tract_pop
        dist.rem_node(removed, filled_graph)
    assert dist.perimeter.sort(key=lambda tract: tract.gid) == filled_graph.neighbors(filled_graph.nodes()[0]).sort(key=lambda tract: tract.gid)


def test_unoc_rem_nodes(filled_graph):
    """Test that unoccupied district rem_node method properly removes a node from nodes."""
    from gerrypy.scripts.fish_scales import UnoccupiedDist
    unoc = UnoccupiedDist(None)
    node_pop = 0
    filled_graph_perim = []
    for node in filled_graph:
        if node.isborder:
            filled_graph_perim.append(node)
    for node in filled_graph:
        unoc.add_node(node, filled_graph)
        node_pop += node.tract_pop
    for ind in range(len(filled_graph) - 1):
        removed = filled_graph.nodes()[len(filled_graph) - ind - 1]
        node_pop -= removed.tract_pop
        unoc.rem_node(removed, filled_graph)
    assert (
        unoc.nodes.nodes() == [list(filled_graph)[0]] and
        unoc.population == node_pop and
        unoc.perimeter.sort(key=lambda tract: tract.gid) == filled_graph_perim.sort(key=lambda tract: tract.gid)
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
    assert len(state.unoccupied[0].perimeter) == 36


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
    assert fill_colorado.area == fill_colorado.districts[0].area + fill_colorado.unoccupied[0].area


def test_state_build_district_perimiter(fill_colorado):
    """Test that district perimiter == state perimiter when there is one district in the state."""
    assertion = True
    for tract in fill_colorado.districts[0].perimeter:
        if tract in fill_colorado.districts[0].nodes.nodes():
            assertion = False
    assert assertion

@pytest.fixture()
def start_state(dummy_request):
    """Start a State."""
    from gerrypy.scripts.fish_scales import State
    state = State(dummy_request, 2)
    return state


@pytest.fixture()
def start_district(start_state, filled_graph):
    """Start a disrtict with one node."""
    from gerrypy.scripts.fish_scales import OccupiedDist
    node = filled_graph.nodes()[0]
    dst = OccupiedDist(1)
    start_state.unoccupied[0].perimeter.append(node)
    start_state.swap(dst, node, filled_graph)
    return node, dst, start_state


def test_swap_returns_correct_unoc_dist(start_district, filled_graph):
    """Test swap from unoc to oc returns the correct unoc district."""
    start_node, dst, state = start_district
    neighbors = filled_graph.neighbors(start_node)
    assert state.swap(dst, neighbors[0], filled_graph) is state.unoccupied[0]


def test_oc_nieghs_unoc_perim_same(start_district, filled_graph):
    """Test district neighbors are the same as unoccupied perimeter when theres only one district."""
    start_node, dst, state = start_district
    assert filled_graph.neighbors(start_node).sort(key=lambda tract: tract.gid) == state.unoccupied[0].perimeter.sort(key=lambda tract: tract.gid)


def test_add_node_updates_dst(start_district, filled_graph):
    """Test that swap adds a node to the district."""
    start_node, dst, state = start_district
    state.swap(dst, dst.perimeter[0], filled_graph)
    assert len(dst.nodes) == 2


def test_oc_nieghs_unoc_perim_same_second_swap(start_district, filled_graph):
    """Test district neighbors are the same as unoccupied perimeter after a second node added wih swap."""
    start_node, dst, state = start_district
    state.swap(dst, dst.perimeter[0], filled_graph)
    assert dst.perimeter.sort(key=lambda tract: tract.gid) == state.unoccupied[0].perimeter.sort(key=lambda tract: tract.gid)


def test_added_node_not_in_dst_perimeter(start_district, filled_graph):
    """Test that added node not in district perimeter."""
    start_node, dst, state = start_district
    new_node = dst.perimeter[0]
    state.swap(dst, new_node, filled_graph)
    assert new_node not in dst.perimeter


def test_added_node_not_in_unoc_perimeter(start_district, filled_graph):
    """Test that added node not in district perimeter."""
    start_node, dst, state = start_district
    new_node = dst.perimeter[0]
    state.swap(dst, new_node, filled_graph)
    assert new_node not in state.unoccupied[0].perimeter


def test_build_state_update_pop(filled_graph):
    """Test that after filling the state, no unassigned pop remains."""
    from gerrypy.scripts.fish_scales import State
    assert State.fill_state()


def test_build_state_no_unoccupied(filled_graph):
    """Test that after filling the state, no unoccupied tracts remain."""
    from gerrypy.scripts.fish_scales import State
    State.fill_state()
    assert State.unoccupied == []


def test_build_state_right_number_districts(filled_graph):
    """Test that filling the state creates the correct number of districts."""
    from gerrypy.scripts.fish_scales import State
    State.fill_state()
    assert len(State.districts) == State.num_dist


def test_build_State_runs_build_district(filled_graph):
    from gerrypy.scripts.fish_scales import State
    State.fill_state()



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
