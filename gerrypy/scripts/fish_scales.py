# Pseudo code:
# This code assumes we will pull the data from our database before constructing the districts, but we could also substitute the node object with a database query.
# Currently, this does not include any criteria for building the districts other than population


class Node(object):
    """Container for information about a given tract to populate District object."""
    def __init__(self, population, neighbors, data):
        self.population = population
        self.neighbors = neighbors
        self.data = data


class District(object):
    """A stucture to contain and separate tracts in a State object."""
    nodes = []
    perimeter = []

    def __init__(self):
        self.population = 0

    def add_node(self, node):
        self.nodes.append(node)
        self.population += node.population
        # delete node and add node’s new neighbors to self.perimeter

    def rem_node(self, node):
        self.population -= node.population
        # remove node’s neighbors from perimeter unless they border another node
        # add node to perimeter


class State(object):
    """Manages how tracts are distributed into districts in a particular state."""
    unoccupied = []
    districts = []
    population = 0

    # Maybe num_dsts rather than dst_num done
    def __init__(self, graph, num_dst):
        # I don’t get this while loop. This doesn’t matter for states like colorado, but for hawaii or michigan, where there are multiple separated areas, we need multiple unoccupied districts.
        while len(self.unoccupied) < len(graph):
            dst = District() # build a district with all nodes connected to (random) starting node
            self.unoccupied.append(dst)
        # self.population = (add populations from unoccupied districts)
        self.num_dst = num_dst

    def build_district(self, start, population):
        dst = District()
        self.districts.append(dst)
        while dst.population < population: #            ← This is vague criteria
            # select the most appropriate node for the district to add
            # if the node borders a separate district or boundary, split the unoccupied district that it is in, and evaluate whether or not node should be added.
            # if appropriate, use dst.add_node() to add the most appropriate node in dst.perimeter
            # else decide the best thing to do             ← This is a BIG step
            pass

    def fill_state(self):
        for num in self.num_dst:
            start = Node(0, [], None) # node in self.districts[-1].perimeter that doesn’t belong to a district and has neighbors from multiple districts or other borders (random node to start)
            # if self.districts is empty, start will be a random border node on 
            self.build_district(start, self.population // self.num_dst)
