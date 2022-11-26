class BFSQ:
    """A queue for BFS / Dijkstra solves"""
    # BFSQ will automatically handle the queue logic for a BFS, Dijkstra, or A* solve
    # for node, weight in q: will loop through nodes in ascending order of weight + heuristic
    # add(node, weight) will add new nodes to the queue, ignoring closed nodes
    # add returns True if node is added to the queue and False if it is closed or redundant
    # heuristic function should take the form heuristic(node, *hargs)
    # nodes and weights are stored in two complementary dicts
    # nodes: dict of node: weight for nodes not yet visited.  Only lowest weight is stored.
    # weights: dict of weight: {nodes} used for sorting / iterating
    def __init__(self, init_nodes=None, heuristic=None, hargs=tuple()):
        self.nodes = {}  # dict of node: weight
        self.weights = {}  # dict of set weight:{nodes}
        self.curr_weight = None  # current minimum weight
        self.closed = {}  # node we've visited
        self.heuristic = heuristic  # Heuristic function for A* (optional)
        self.heuristic_cache = {}  # Cache of node:heuristic value
        self.hargs = hargs  # Arguments for heuristic function (optional)

        if isinstance(init_nodes, dict):  # add all node: weight pairs in dict
            for node, weight in init_nodes.items():
                self.add(node, weight)
        elif isinstance(init_nodes, set) or isinstance(init_nodes, list):  # add nodes in iterable with weight 0
            for node in init_nodes:
                self.add(node, 0)
        else:  # add node wth weight 0
            self.add(init_nodes, 0)

    def add(self, node, weight):
        if node in self.closed:  # don't add closed node
            return False  # node was not added
        if self.heuristic is None:  # apply heuristic if applicable
            heur = 0
        elif node in self.heuristic_cache:  # check cache first
            heur = self.heuristic_cache[node]
        else:
            heur = self.heuristic(node, *self.hargs)
            self.heuristic_cache[node]=heur
        sort_weight = heur + weight
        if node in self.nodes:  # if this node is already in queue, check which has lower weight
            old_weight = self.nodes[node]
            if weight < old_weight:  # if the new weight is lower, remove the old instance
                old_sort_weight = old_weight + heur
                self.weights[old_sort_weight].discard(node)
                if not self.weights[old_sort_weight]:
                    self.weights.pop(old_sort_weight)
            else:  # otherwise, don't add to the queue
                return False
        if sort_weight not in self.weights:  # add node to weights
            self.weights[sort_weight] = {node}
        else:
            self.weights[sort_weight].add(node)
        self.nodes[node] = weight  # add node to nodes
        return True  # yes, we did add this to the queue

    def __iter__(self):
        return self

    def __next__(self):
        if self.weights:
            if self.curr_weight is None:  # if the current min weight has been exhausted, find the next
                self.curr_weight = min(self.weights.keys())
            nodes_at_curr_weight = self.weights[self.curr_weight]
            next_node = nodes_at_curr_weight.pop()
            next_weight = self.nodes.pop(next_node)
            self.closed[next_node] = next_weight
            if not nodes_at_curr_weight:  # remove current weight if it's empty
                self.weights.pop(self.curr_weight)
                self.curr_weight = None
            return next_node, next_weight
        else:  # nothing left, break loop
            raise StopIteration
