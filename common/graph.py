import dancer


class Graph:
    def __init__(self, default=dict):
        self.graph = {}
        self.default = default

    def add_node(self, node):
        if node in self.graph:
            return False
        else:
            self.graph[node] = self.default()
            return True

    def rem_node(self, node):
        if node in self.graph:
            self.graph.pop(node)
            return True
        else:
            return False

    def add_edge_eq(self, a, b, weight=1):
        self.add_node(a)
        self.add_node(b)
        self.graph[a].update({b:weight})
        self.graph[b].update({a:weight})

    def add_edge_neq(self, a, b, weight=1):
        for node in (a, b):
            if node not in self.graph:
                self.graph[node] = self.default()
        self.graph[a].update({b:weight})

    def make_edges(self, fun):
        for node, edges in self.graph.items():
            edges.update(fun(self, node))

    def dijkstra(self, start, targets, all_paths=False, full_paths=False):
        # find the shortest path from start to targets
        # if multiple paths are tied for shortest, return them all
        # targets must be an iterable, preferably a set, even if it's just one target
        # if all_paths, return paths to all points in graph, else only paths with min weight
        # if full_paths, return tuple of points in path, else return just the path weight
        if not isinstance(targets, set):
            targets = set(targets)
        assert start in self.graph, 'Start not in graph'
        assert len(targets & self.graph.keys()) > 0, 'Target(s) not in graph'
        queue = {(0, start)}
        closed = set()
        last_weight = None
        parents = {}
        solutions = {}

        while queue:
            curr_item = min(queue)
            queue.remove(curr_item)
            curr_weight, curr_loc = curr_item
            if curr_loc not in closed and all_paths or (last_weight is None or curr_weight <= last_weight):
                closed.add(curr_loc)
                if curr_loc in targets:
                    solutions[curr_loc] = curr_weight
                    last_weight = curr_weight
                if all_paths or curr_loc not in targets:
                    for new_loc, new_weight in self.graph[curr_loc].items():
                        if new_loc not in closed:
                            new_weight = curr_weight + new_weight
                            queue.add((new_weight, new_loc))
                            parents[new_loc] = curr_loc

        if full_paths:
            paths = []
            for loc in solutions.keys():
                path = [loc]
                while loc in parents:
                    loc = parents[loc]
                    path.append(loc)
                paths.append(tuple(reversed(path)))
            return tuple(paths)
        else:
            return solutions

