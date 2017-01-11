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

    def __init__(self, districtID, tracts=None):
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
        node.districtid = self.districtID
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


class UnoccupiedDist(OccupiedDist):
    """A structure to contain tracts that haven't been claimed by a district.

    add_node(self, node): adds node to nodes and updates district
    properties accordingly

    rem_node(self, node): removes node from nodes and updates district
    properties accordingly
    """

    def __init__(self, districtID, tracts=None):
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
        node.districtid = None
        self.nodes.add_node(node)
        self.population += node.tract_pop
        self.area += node.shape_area
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
        self.area -= node.shape_area
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
        self.num_dst = num_dst
        global TRACTGRAPH
        TRACTGRAPH = fill_graph(request)
        landmass = nx.connected_components(TRACTGRAPH)
        for island in landmass:
            unoc = UnoccupiedDist(None, island)
            self.population += unoc.population
            self.unoccupied.append(unoc)
            self.area += unoc.area
        self.target_pop = self.population // num_dst

        # construct target districts

    def build_district(self, tgt_population, dist_num, graph=TRACTGRAPH):
        """Create a new district stemming from the start node with a given population."""
        building = True
        dst = OccupiedDist(dist_num)
        self.districts.append(dst)
        start = self.find_start()
        self.swap(dst, start, graph)
        while building:
            new_tract = self.select_next(start, dst)
            if new_tract is None:
                break
            high_pop = (new_tract.population + dst.population)
            if abs(high_pop - tgt_population) > abs(dst.population - tgt_population):
                break
            else:
                unoc_dst = self.swap(dst, new_tract, graph)
                neighbors = graph.neighbors(new_tract)
                unassigned_neighbors = [neighbor for neighbor in neighbors if neighbor in unoc_dst]
                if len(unassigned_neighbors) > 1:
                    for i in range(len(unassigned_neighbors)):
                        if not nx.has_path(
                            unoc_dst.nodes,
                            unassigned_neighbors[i],
                            unassigned_neighbors[i - 1]
                        ):
                            unoc_dst.rem_node(new_tract, graph)
                            dst.add_node(new_tract, graph)
                            building = False

    def swap(self, dst, new_tract, graph):
        """Exchange tract from unoccupied district to district"""
        unoc_dst = None
        for island in self.unoccupied:
            if new_tract in island.perimeter:
                unoc_dst = island
        unoc_dst.rem_node(new_tract)
        dst.add_node(new_tract, graph)
        return unoc_dst

    # def shift_dist(self, dst):
    #     """Move build district into the smallest bordering unoccupied district
    #     until all bordering unoccupied district populations are divisible by target population."""

    def select_next(self, dst, start=None, graph=TRACTGRAPH):
        """Choose the next best tract to add to growing district."""
        if start:
            return start
        best_count = 0
        best = None
        for perimeter_tract in dst.perimeter:
            if perimeter_tract.districtid is None:
                count = 0
                for neighbor in graph.neighbors(perimeter_tract):
                    if neighbor.districtid == dst.districtID:
                        count += 1
                if count > best_count:
                    best_count = count
                    best = perimeter_tract
        return best

    def fill_state(self, graph=TRACTGRAPH):
        """Build districts until all unoccupied tracts are claimed."""

        rem_pop = 0
        for unoc in self.unoccupied:
            rem_pop += unoc.population
        rem_dist = self.num_dst - len(self.districts)
        tgt_population = rem_pop / rem_dist
        for num in range(self.num_dst):
            self.build_district(tgt_population, num + 1)

    def find_start(self, graph=TRACTGRAPH):
        """."""
        best_set = set()
        best = None
        for tract in self.unoccupied[0].perimeter:
            unique_dists = set()
            for neighbor in graph.neighbors(tract):
                for dst in self.districts:
                    if neighbor in dst.nodes.nodes():
                        unique_dists.add(dst)
            if len(unique_dists) > len(best_set) or len(unique_dists) == 0:
                best_set = unique_dists
                best = tract
        return best


    def split_unoccupied(self):
        pass

    def splits_unoccupied(self, tract):
        add, splits = True, False
        return {'add': add, 'splits': splits}

    def split_unoccupied_dist(self, dist):
        """Removes unoccupied dist from State and adds contiguous unoccupied sub-districts."""
        self.unoccupied.remove(dist)
        new_iters = nx.connected_components(dist.nodes)
        new_dists = []
        for itr in new_iters:
            new_dists.append(UnoccupiedDist(None, itr))
        self.unoccupied.extend(new_dists)

       # dont_add = set()
        # dst = OccupiedDist()
        # self.districts.append(dst)
        # while True:
        #     new_tract = self.select_next(dst, dont_add)
        #     high_pop = (new_tract.population + dst.population)
        #     if abs(high_pop - tgt_population) > abs(dst.population - tgt_population):
        #         break
        #     else:
        #         unoc_dst = None
        #         for unoc in self.unoccupied:
        #             if new_tract in unoc.perimeter:
        #                 unoc_dst = unoc
        #         unoc_dst.rem_node(new_tract)
        #         dst.add_node(new_tract, graph)
        #         neighbors = graph.neighbors(new_tract)
        #         unassigned_neighbors = [neighbor for neighbor in neighbors if neighbor in unoc_dst]
        #         if len(unassigned_neighbors) > 1:
        #             for i in range(len(unassigned_neighbors)):
        #                 if not nx.has_path(
        #                         unoc_dst.nodes,
        #                         unassigned_neighbors[i],
        #                         unassigned_neighbors[i - 1]
        #                     ):
        #                     unoc_dst.add_node(new_tract, graph)
        #                     dst.rem_node(new_tract, graph)
        #                     dont_add.add(new_tract)
