"""Contains objects to pull tract information from database,
compute new congressional districts,
and store new information in a separate table."""
from gerrypy.models.mymodel import Tract, Edge
import networkx as nx


TRACTGRAPH = None


def fill_graph(request):
    """Build global graph from tract and edge databases."""
    graph = nx.Graph()
    tracts = request.dbsession.query(Tract).all()  # get all tracts from db
    edges = request.dbsession.query(Edge).all()  # get all edges from db

    for tract in tracts:
        graph.add_node(tract)
    for edge in edges:
        source = request.dbsession.query(Tract).get(edge.tract_source)
        target = request.dbsession.query(Tract).get(edge.tract_target)
        graph.add_edge(source, target)
    return graph


# class Node(object):
#     """Container for information about a given tract to populate District object."""

#     def __init__(self, population, data):
#         """Duh."""
#         self.population = population
#         self.data = data
#         self.neighbors = []

#     def add_neighbors(self, neighbors):
#         """Add a list of nodes adjacent to self."""
#         self.neighbors.extend(neighbors)


class District(object):
    """A stucture to contain and separate tracts in a State object.

    add_node(self, node): adds node to nodes and updates district
    properties accordingly

    rem_node(self, node): removes node from nodes and updates district
    properties accordingly
    """

    nodes = []
    perimeter = []

    def __init__(self, tracts=None):
        """."""
        self.population = 0
        if tracts:
            try:
                for tract in tracts:
                    self.add_node(tract)
            except TypeError:
                raise TypeError('Tracts must be iterable.')

    def add_node(self, node):
        """Add node to nodes and updates district properties accordingly."""
        self.nodes.append(node)
        self.population += node.tract_pop
        if self.perimeter:
            import pdb; pdb.set_trace()
            self.perimeter.remove(node)
        neighbors = TRACTGRAPH.neighbors(node)
        for neighbor in neighbors:
            if neighbor not in self.nodes and neighbor not in self.perimeter:
                self.perimeter.append(neighbor)

    def rem_node(self, node):
        """Remove node from nodes and updates district properties accordingly."""
        self.population -= node.tract_pop
        self.perimeter.append(node)
        self.nodes.remove(node)
        neighbors = TRACTGRAPH.neighbors(node)
        for neighbor in neighbors:
            takeout = True
            if neighbor in self.perimeter:
                neighborneighbors = TRACTGRAPH.neighbors(neighbor)
                for neighborneighbor in neighborneighbors:
                    if neighborneighbor in self.nodes:
                        takeout = False
            if takeout:
                self.perimeter.remove(neighbor)


class State(object):
    """Manages how tracts are distributed into districts in a particular state.

    build_district(self, start, population):
    creates a new district stemming from the start node with a given population

    fill_state(self): continues to build districts until all unoccupied tracts are claimed
    """

    unoccupied = []
    districts = []
    population = 0

    def __init__(self, request, num_dst):
        """Build unoccupied district(s) for entire state."""
        global TRACTGRAPH
        TRACTGRAPH = fill_graph(request)
        landmass = nx.connected_components(TRACTGRAPH)
        for island in landmass:
            self.unoccupied.append(District(island))

        # construct target districts

    def build_district(self, start, population):
        """Create a new district stemming from the start node with a given population."""
        dst = District()
        self.districts.append(dst)
        while dst.population < population_share:  # ← This is vague criteria
            # select the most appropriate node for the district to add

            # if the node borders a separate district or boundary,
            # split the unoccupied district that it is in,
            # and evaluate whether or not node should be added.

            # if appropriate, use dst.add_node() to add the most appropriate node in dst.perimeter
            # else decide the best thing to do             ← This is a BIG step
            pass

    # def fill_state(self):
    #     """Build districts until all unoccupied tracts are claimed."""
    #     for num in range(self.num_dst):
    #         start = Node(0, [], None)  # node in self.districts[-1].perimeter
    #         # that doesn't belong to a district and has neighbors
    #         # from multiple districts or other borders (random node to start)

    #         # if self.districts is empty, start will be a random border node on
    #         self.build_district(start, self.population // self.num_dst)
