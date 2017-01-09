"""Tests for GerryPy database and district-building algorithm."""


import pytest
from gerrypy.scripts.fish_scales import Node


# Algorithm tests
NEIGHBORS = [
    Node(1, [], None),
    Node(100, [], ["data"]),
]


NODES = [
    [123456, [], None],
    [200000, [], []],
    [200000, [NEIGHBORS[0], NEIGHBORS[1]], ["data"]],
]


BAD_POP = [
    [0, [], []],
    [-123456, [], []],
]


BAD_NEIGH = [
    [100000, None, ["data"]],
    [100000, [1, 2, 3], ["data"]],
    [100000, ["four", "five", "six"], ["data"]],
]


NODE_LST = [
    [[], [], 0],
    [[Node(1, [], ["data"])], [], 1],
    [[Node(1, [], ["data"]), Node(10, [], ["more data"])], [], 11],
    [[Node(1, [], ["data"]), Node(10, [NEIGHBORS[0]], None)], [NEIGHBORS[0]], 11],
    [[NEIGHBORS[0], NODES[2]], [NEIGHBORS[1]], 200001],
    [[Node(1, [NEIGHBORS[0]], ["data"]), NODES[2]], [NEIGHBORS[0], NEIGHBORS[1]], 2]
]


BAD_NODES = [None, object, "string", 42, [], {}, [Node(1, [], None)]]


@pytest.mark.parametrize("pop, neigh, data", NODES)
def test_node_constructor(pop, neigh, data):
    """Tests that node constructor can contain population as a property."""
    node = Node(pop, neigh, data)
    assert (
        node.population == pop and
        node.neighbors == neigh and
        node.data == data
    )


@pytest.mark.parametrize("pop, neigh, data", BAD_POP)
def test_node_population_error(pop, neigh, data):
    """Tests that node constructor raises an error when given a negative population."""
    with pytest.raises(ValueError):
        Node(pop, neigh, data)


@pytest.mark.parametrize("pop, neigh, data", BAD_NEIGH)
def test_node_neighbors_error(pop, neigh, data):
    """Tests that node constructor raises an error when given neighbors that are not node."""
    with pytest.raises(ValueError):
        Node(pop, neigh, data)


def test_district_constructor():
    """Tests that district constructor creates properties for population, nodes, and perimeters."""
    from gerrypy.scripts.fish_scales import District
    dist = District()
    assert (
        dist.nodes == [] and
        dist.perimeter == [] and
        dist.population == 0
    )


@pytest.mark.parametrize("node_lst, peri_lst, pop", NODE_LST)
def test_district_add_node(node_lst, peri_lst, pop):
    """Tests that district add_node method properly adds a node to nodes."""
    from gerrypy.scripts.fish_scales import District
    dist = District()
    for node in node_lst:
        dist.add_node(node)
    assert (
        dist.nodes == node_lst and
        dist.perimeter == peri_lst and
        dist.population == pop
    )


@pytest.mark.parametrize("bad_node", BAD_NODES)
def test_district_add_node_error(bad_node):
    """Tests that district add_node method raises an error when a non-node object is put into it."""
    from gerrypy.scripts.fish_scales import District
    dist = District()
    with pytest.raises(ValueError):
        dist.add_node(bad_node)


# def test_district_rem_node():
#     """Tests that district rem_node properly removes a node from nodes."""
#     from gerrypy.scripts.fish_scales import District
#     dist = District()
#     node_lst = [Node(1, [], "data") * 10]
#     for node in node_lst:
#         dist.add_node(node)
#     assert (
#         dist.nodes == node_lst and
#         dist.perimeter == [] and
#         dist.population == 10
#     )
