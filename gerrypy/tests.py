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

@pytest.mark.parametrize("pop, neigh, data", NODES)
def test_node_properties(pop, neigh, data):
    """Tests that node constructor can contain population as a property."""
    node = Node(pop, neigh, data)
    assert node.population == pop and node.neighbors == neigh and node.data == data


@pytest.mark.parametrize("pop, neigh, data", BAD_POP)
def test_node_bad_population(pop, neigh, data):
    """Tests that node constructor can contain population as a property."""
    with pytest.raises(ValueError):
        Node(pop, neigh, data)


@pytest.mark.parametrize("pop, neigh, data", BAD_NEIGH)
def test_node_bad_neighbors(pop, neigh, data):
    """Tests that node constructor can contain population as a property."""
    with pytest.raises(ValueError):
        Node(pop, neigh, data)
