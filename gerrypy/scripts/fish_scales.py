# -*- coding: utf-8 -*-
"""
Contains objects to pull tract information from database,
compute new congressional districts,
and store new information in a separate table.
"""
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


class OccupiedDist(object):
    """A stucture to contain and separate tracts in a State object.

    add_node(self, node): adds node to nodes and updates district
    properties accordingly

    rem_node(self, node): removes node from nodes and updates district
    properties accordingly
    """

    def __init__(self, tracts=None, districtID=None):
        """."""
        self.nodes = nx.Graph()
        self.perimeter = []
        self.population = 0
        self.area = 0
        self.districtID = districtID
        if tracts:
            try:
                for tract in tracts:
                    self.add_node(tract, TRACTGRAPH)
            except TypeError:
                raise TypeError('Tracts must be iterable.')

    def add_node(self, node, graph):
        """Add node to nodes and updates district properties accordingly."""
        self.nodes.add_node(node)
        edge_lst = graph.neighbors(node)
        for edge in edge_lst:
            if edge in self.nodes.nodes():
                self.nodes.add_edge(edge, node)
        self.population += node.tract_pop
        self.area += node.shape_area
        if node in self.perimeter:
            self.perimeter.remove(node)
        neighbors = graph.neighbors(node)
        for neighbor in neighbors:
            if neighbor not in self.nodes.nodes() and neighbor not in self.perimeter:
                self.perimeter.append(neighbor)

    def rem_node(self, node, graph):
        """Remove node from nodes and updates district properties accordingly."""
        self.population -= node.tract_pop
        self.nodes.remove_node(node)
        self.area -= node.shape_area
        neighbors = graph.neighbors(node)
        to_perimeter = False
        for neighbor in neighbors:
            takeout = True
            if neighbor in self.perimeter:
                neighborneighbors = graph.neighbors(neighbor)
                for neighborneighbor in neighborneighbors:
                    if neighborneighbor in self.nodes.nodes():
                        takeout = False
                if takeout:
                    self.perimeter.remove(neighbor)
            elif neighbor in self.nodes.nodes():
                to_perimeter = True
        if to_perimeter:
            self.perimeter.append(node)
        # if len(self.nodes) == 1:
        #     import pdb; pdb.set_trace()


class UnoccupiedDist(OccupiedDist):
    """A structure to contain tracts that haven't been claimed by a district.

    add_node(self, node): adds node to nodes and updates district
    properties accordingly

    rem_node(self, node): removes node from nodes and updates district
    properties accordingly
    """

    def add_node(self, node, graph):
        """Add node to nodes and updates district properties accordingly."""
        self.nodes.add_node(node)
        self.population += node.tract_pop
        neighbors = graph.neighbors(node)
        to_add = False
        for neighbor in neighbors:
            takeout = True
            if neighbor in self.perimeter:
                neighborneighbors = graph.neighbors(neighbor)
                for neighborneighbor in neighborneighbors:
                    if neighborneighbor not in self.nodes:
                        takeout = False
                if takeout:
                    self.perimeter.remove(neighbor)
            if neighbor not in self.nodes:
                to_add = True
        if to_add:
            self.perimeter.append(node)

    def rem_node(self, node, graph):
        """Remove node from nodes and updates district properties accordingly."""
        self.nodes.remove_node(node)
        self.population -= node.tract_pop
        if node in self.perimeter:
            self.perimeter.remove(node)
        neighbors = graph.neighbors(node)
        for neighbor in neighbors:
            if neighbor not in self.nodes and neighbor not in self.perimeter:
                self.perimeter.append(neighbor)


class State(object):
    """Manages how tracts are distributed into districts in a particular state.

    build_district(self, start, population):
    creates a new district stemming from the start node with a given population

    fill_state(self): continues to build districts until all unoccupied tracts are claimed
    """

    def __init__(self, request, num_dst):
        """Build unoccupied district(s) for entire state."""
        self.unoccupied = []
        self.districts = []
        self.population = 0
        self.area = 0
        global TRACTGRAPH
        TRACTGRAPH = fill_graph(request)
        landmass = nx.connected_components(TRACTGRAPH)
        for island in landmass:
            dist = OccupiedDist(island)
            self.population += dist.population
            self.unoccupied.append(dist)
            self.area += dist.area
        self.target_pop = self.population // num_dst

        # construct target districts

    def build_district(self, start, tgt_population, graph=TRACTGRAPH):
        """Create a new district stemming from the start node with a given population."""
        dst = OccupiedDist()
        self.districts.append(dst)
        while True:
            new_tract = State.select_next(dst)
            if abs((new_tract.population + dst.population) - tgt_population) > abs(dst.population - tgt_population):
                break
            else:
                unoc_dst = None
                for unoc in self.unoccupied:
                    if new_tract in unoc.perimeter:
                        unoc_dst = unoc
                unoc_dst.rem_node(new_tract)
                dst.add_node(new_tract, graph)
                neighbors = graph.neighbors(new_tract)
                unassigned_neighbors = [neighbor for neighbor in neighbors if neighbor in unoc_dst]
                if len(unassigned_neighbors) > 1:
                    for i in range(len(unassigned_neighbors)):
                        if not nx.has_path(unoc_dst.nodes, unassigned_neighbors[i], unassigned_neighbors[i - 1]):
                            self.split_unoccupied_dist(unoc)
                            


        while dst.population < (self.target_pop - 1000):
            dont_add = set()
            new_tract = State.select_next(dst)
            if new_tract is None:
                break
            # not implemented yet
            answer = self.splits_unoccupied(new_tract)
            if answer['add']:
                dst.add_node(new_tract)
                for unoc_dst in self.unoccupied:
                    if new_tract in unoc_dst.nodes:
                        unoc_dst.rem_node(new_tract)
            else:
                dont_add.add(new_tract)
                continue

        # while dst.population < population_share:  # ← This is vague criteria
        #     # select the most appropriate node for the district to add

        #     # if the node borders a separate district or boundary,
        #     # split the unoccupied district that it is in,
        #     # and evaluate whether or not node should be added.

        #     # if appropriate, use dst.add_node() to add the most appropriate node in dst.perimeter
        #     # else decide the best thing to do             ← This is a BIG step
        #     pass

    def fill_state(self):
        """Build districts until all unoccupied tracts are claimed."""

        # find starting tract
        def sort_by(tract):
            return len(set(map(lambda x: x.districtID, TRACTGRAPH.neighbors(tract))))
        unoc_perimeter = sorted(self.unoccupied.perimeter, key=sort_by)
    #     for num in range(self.num_dst):
    #         start = Node(0, [], None)  # node in self.districts[-1].perimeter
    #         # that doesn't belong to a district and has neighbors
    #         # from multiple districts or other borders (random node to start)

    #         # if self.districts is empty, start will be a random border node on
    #         self.build_district(start, self.population // self.num_dst)

    def split_unoccupied(self):
        pass

    def splits_unoccupied(self, tract):
        add, splits = True, False
        return {'add': add, 'splits': splits}

    @staticmethod
    def select_next(dst):
        """Choose the next best tract to add to growing district."""
        best_count = 0
        best = None
        for perimeter_tract in dst.perimeter:
            if perimeter_tract.districtID is None:
                count = 0
                for neighbor in perimeter_tract.neighbors():
                    if neighbor.districtID == dst.district_number:
                        count += 1
                if count > best_count:
                    best_count = count
                    best = perimeter_tract
        return best

    def split_unoccupied_dist(self, dist):
        """Removes unoccupied dist from State and adds contiguous unoccupied sub-districts."""
        self.unoccupied.remove(dist)
        new_graphs = nx.connected_components(dist.nodes)
        new_dists = []
        for graph in new_graphs:
            new_dists.append(UnoccupiedDist(graph))
        self.unoccupied.extend(new_dists)
