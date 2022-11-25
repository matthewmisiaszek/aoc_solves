class BFSQ:
    """A queue for BFS / Dijkstra solves"""
    def __init__(self, init_nodes=None):
        if init_nodes is None:
            self.nodes = {}
            self.curr_weight = None
        else:
            self.nodes = init_nodes.copy()
            self.curr_weight = min(self.nodes.values())
        self.weights = {}
        for node, weight in self.nodes.items():
            if weight not in self.weights:
                self.weights[weight] = {node}
            else:
                self.weights[weight].add(node)
        self.closed = {}

    def add(self, node, weight):
        if node in self.closed:
            return False
        if node in self.nodes:
            old_weight = self.nodes[node]
            if weight < old_weight:
                self.weights[old_weight].discard(node)
                if not self.weights[old_weight]:
                    self.weights.pop(old_weight)
            else:
                return False
        if weight not in self.weights:
            self.weights[weight] = {node}
        else:
            self.weights[weight].add(node)
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
            next_weight = self.curr_weight
            self.closed[next_node] = next_weight
            self.nodes.pop(next_node)
            if not nodes_at_curr_weight:
                self.weights.pop(self.curr_weight)
                self.curr_weight = None
            return next_node, next_weight
        else:
            raise StopIteration
