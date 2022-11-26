class BFSQ:
    """A queue for BFS / Dijkstra solves"""
    def __init__(self, init_nodes=None, heuristic=None, hargs=tuple()):
        self.closed = {}
        self.heuristic = heuristic
        self.heuristic_cache = {}
        self.hargs = hargs
        self.nodes = {}
        self.weights = {}
        self.curr_weight = None
        if isinstance(init_nodes, dict):
            for node, weight in init_nodes.items():
                self.add(node, weight)
        elif isinstance(init_nodes, set) or isinstance(init_nodes, list):
            for node in init_nodes:
                self.add(node, 0)
        else:
            self.add(init_nodes, 0)

    def add(self, node, weight):
        if node in self.closed:
            return False
        if self.heuristic is None:
            heur = 0
        elif node in self.heuristic_cache:
            heur = self.heuristic_cache[node]
        else:
            heur = self.heuristic(node, *self.hargs)
            self.heuristic_cache[node]=heur
        hweight = heur + weight
        if node in self.nodes:
            old_weight = self.nodes[node]
            if weight < old_weight:
                hold_weight = old_weight + heur
                self.weights[hold_weight].discard(node)
                if not self.weights[hold_weight]:
                    self.weights.pop(hold_weight)
            else:
                return False
        if hweight not in self.weights:
            self.weights[hweight] = {node}
        else:
            self.weights[hweight].add(node)
        self.nodes[node] = weight
        return True

    def __iter__(self):
        return self

    def __next__(self):
        if self.weights:
            if self.curr_weight is None:
                self.curr_weight = min(self.weights.keys())
            nodes_at_curr_weight = self.weights[self.curr_weight]
            next_node = nodes_at_curr_weight.pop()
            next_weight = self.nodes.pop(next_node)
            self.closed[next_node] = next_weight
            # self.nodes.pop(next_node)
            if not nodes_at_curr_weight:
                self.weights.pop(self.curr_weight)
                self.curr_weight = None
            return next_node, next_weight
        else:
            raise StopIteration
