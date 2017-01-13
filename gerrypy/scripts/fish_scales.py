"""
Contains objects to pull tract information from database,
compute new congressional districts,
and store new information in a separate table.
"""
from gerrypy.models.mymodel import Tract, Edge
import networkx as nx


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

    def __init__(self, districtID, state_graph, tracts=None):
        """."""
        self.nodes = nx.Graph()
        self.perimeter = []
        self.population = 0
        self.area = 0
        self.districtID = districtID
        if tracts:
            try:
                for tract in tracts:
                    self.add_node(tract, state_graph)
            except TypeError:
                raise TypeError('Tracts must be iterable.')

    def add_node(self, node, state_graph):
        """Add node to nodes and updates district properties."""
        node.districtid = self.districtID
        self.nodes.add_node(node)
        for edge in state_graph.neighbors(node):
            if edge in self.nodes.nodes():
                self.nodes.add_edge(edge, node)
        self.population += node.tract_pop
        self.area += node.shape_area
        if node in self.perimeter:
            self.perimeter.remove(node)
        neighbors = state_graph.neighbors(node)
        for neighbor in neighbors:
            if neighbor not in self.nodes.nodes() and neighbor not in self.perimeter:
                self.perimeter.append(neighbor)

    def rem_node(self, node, state_graph):
        """Remove node from nodes and updates district properties."""
        self.population -= node.tract_pop
        self.nodes.remove_node(node)
        self.area -= node.shape_area
        neighbors = state_graph.neighbors(node)
        to_perimeter = False
        for neighbor in neighbors:
            takeout = True
            if neighbor in self.perimeter:
                neighborneighbors = state_graph.neighbors(neighbor)
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

    def __init__(self, districtID, state_graph, tracts=None):
        """."""
        self.nodes = nx.Graph()
        self.perimeter = []
        self.population = 0
        self.area = 0
        self.districtID = districtID
        if tracts:
            try:
                for tract in tracts:
                    self.add_node(tract, state_graph)
            except TypeError:
                raise TypeError('Tracts must be iterable.')

    def add_node(self, node, state_graph):
        """Add node to nodes and updates district properties accordingly."""
        node.districtid = None
        self.nodes.add_node(node)
        for neighbor in state_graph.neighbors(node):
            if neighbor in self.nodes:
                self.nodes.add_edge(neighbor, node)
        self.population += node.tract_pop
        self.area += node.shape_area
        neighbors = state_graph.neighbors(node)
        to_add = False
        for neighbor in neighbors:
            takeout = True
            if neighbor in self.perimeter:
                neighborneighbors = state_graph.neighbors(neighbor)
                for neighborneighbor in neighborneighbors:
                    if neighborneighbor not in self.nodes:
                        takeout = False
                if takeout:
                    self.perimeter.remove(neighbor)
            if neighbor not in self.nodes:
                to_add = True
        if to_add:
            self.perimeter.append(node)

    def rem_node(self, node, state_graph):
        """Remove node from nodes and updates district properties accordingly."""
        self.population -= node.tract_pop
        self.area -= node.shape_area
        if node in self.perimeter:
            self.perimeter.remove(node)
        neighbors = self.nodes.neighbors(node) #state_graph.neighbors(node)
        for neighbor in neighbors:
            if neighbor not in self.perimeter:
                self.perimeter.append(neighbor)
        self.nodes.remove_node(node)


class State(object):
    """Manages how tracts are distributed into districts in a particular state.

    build_district(self, start, population):
    creates a new district stemming from the start node with a given population

    fill_state(self, request): continues to build districts until all unoccupied tracts are claimed
    """

    def __init__(self, request, num_dst):
        """Build unoccupied district(s) for entire state."""
        self.unoccupied = []
        self.districts = []
        self.population = 0
        self.area = 0
        self.num_dst = num_dst
        self.state_graph = fill_graph(request)
        landmass = nx.connected_components(self.state_graph)
        for island in landmass:
            unoc = UnoccupiedDist(None, self.state_graph, tracts=island)
            for tract in unoc.nodes.nodes():
                if tract.isborder == 1:
                    unoc.perimeter.append(tract)
            self.population += unoc.population
            self.unoccupied.append(unoc)
            self.area += unoc.area
        self.target_pop = self.population // num_dst

    def fill_state(self, request, criteria):
        """Build districts until all unoccupied tracts are claimed."""
        from gerrypy.graph_db_interact.assigndistrict import assign_district, populate_district_table

        for num in range(self.num_dst):
            rem_pop = 0
            for unoc in self.unoccupied:
                rem_pop += unoc.population
            rem_dist = self.num_dst - len(self.districts)
            tgt_population = rem_pop / rem_dist
            self.build_district(tgt_population, num + 1, criteria)
        assign_district(request, self.state_graph)
        populate_district_table(request, self)
        if self.unoccupied:
            return False
        return True

    def build_district(self, tgt_population, dist_num, criteria):
        """Create a new district stemming from the start node with a given population."""
        dst = OccupiedDist(dist_num, self.state_graph)
        self.districts.append(dst)
        start = self.find_start()
        self.swap(dst, start) #if state is full, this wont work
        while True:
            new_tract = self.select_next(dst, criteria)
            if new_tract is None:
                for unoc in self.unoccupied:
                    if not len(unoc.nodes.nodes()):
                        self.unoccupied.remove(unoc)
                break
            high_pop = (new_tract.tract_pop + dst.population)
            if abs(high_pop - tgt_population) > abs(dst.population - tgt_population):
                break
            else:
                self.swap(dst, new_tract)
                neighbors = self.state_graph.neighbors(new_tract)
                unassigned_neighbors = [neighbor for neighbor in neighbors if neighbor in self.unoccupied[0].nodes]
                if len(unassigned_neighbors) > 1:
                    for i in range(len(unassigned_neighbors)):
                        if not nx.has_path(
                            self.unoccupied[0].nodes,
                            unassigned_neighbors[i],
                            unassigned_neighbors[i - 1]
                        ):
                            unoc_neighbors = [x for x in nx.connected_components(self.unoccupied[0].nodes)]
                            biggest = max(unoc_neighbors, key=lambda x: len(x))
                            unoc_neighbors.remove(biggest)

                            for neigh in unoc_neighbors:
                                for tract in neigh:
                                    self.swap(dst, tract)
                            break

    def swap(self, dst, new_tract):
        """Exchange tract from unoccupied district to district."""
        # unoc_dst = None
        # for island in self.unoccupied:
        #     if new_tract in island.perimeter:
        #         unoc_dst = island
        self.unoccupied[0].rem_node(new_tract, self.state_graph)
        dst.add_node(new_tract, self.state_graph)
        # return unoc_dst

    def select_next(self, dst, criteria):
        """Choose the next best tract to add to growing district."""
        best_rating = 0
        best = None
        for perimeter_tract in dst.perimeter:
            if perimeter_tract.districtid is None:
                count = 0
                for neighbor in self.state_graph.neighbors(perimeter_tract):
                    if neighbor.districtid == dst.districtID:
                        count += 1
                counties = set()
                for node in dst.nodes:
                    counties.add(node.county)
                same_county = 0
                if perimeter_tract.county in counties:
                    same_county = 1
                rating = count * int(criteria['compactness']) + same_county * int(criteria['county'])
                if rating > best_rating:
                    best_rating = rating
                    best = perimeter_tract
        return best

    def find_start(self):
        """
        Choose best starting tract for a new district.
        Based on number of bordering districts.
        """
        best_set = set()
        best = None
        for tract in self.unoccupied[0].perimeter:
            unique_dists = set()
            for neighbor in self.state_graph.neighbors(tract):
                for dst in self.districts:
                    if neighbor in dst.nodes.nodes():
                        unique_dists.add(dst)
            if len(unique_dists) > len(best_set) or len(unique_dists) == 0:
                best_set = unique_dists
                best = tract
        return best

    def split_unoccupied_dist(self, unoc_dst):
        """Remove unoccupied dist from State and adds contiguous unoccupied sub-districts."""
        self.unoccupied.remove(unoc_dst)
        index = len(self.unoccupied)
        landmass = nx.connected_components(unoc_dst.nodes)
        for island in landmass:
            self.unoccupied.append(UnoccupiedDist(None, self.state_graph, tracts=island))
        return self.unoccupied[index:]
