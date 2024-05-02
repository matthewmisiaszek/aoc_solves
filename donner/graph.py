import blitzen
from donner import spatial
from donner.bfsqueue import BFSQ


class Graph(dict):
    def __init__(self, default=dict):
        super().__init__()
        self.graph = self  # I first wrote this before I knew about subclassing
        self.default = default

    def add_node(self, node):
        if node in self:
            return False
        else:
            self[node] = self.default()
            return True

    def rem_node(self, node):
        if node in self:
            self.pop(node)
            return True
        else:
            return False

    def add_edge_eq(self, a, b, weight=1):
        self.add_node(a)
        self.add_node(b)
        self[a].update({b: weight})
        self[b].update({a: weight})

    def add_edge_neq(self, a, b, weight=1):
        for node in (a, b):
            if node not in self:
                self[node] = self.default()
        self[a].update({b: weight})

    def make_edges(self, fun):
        for node, edges in self.items():
            edges.update(fun(self, node))

    def contract(self, keep=()):
        for node in tuple(self.keys()):
            if len(self[node]) != 2 or node in keep:
                continue
            a, b = tuple(self[node].keys())
            if node in self[a]:
                self[a][b] = self[a][node] + self[node][b]
                self[a].pop(node)
            if node in self[b]:
                self[b][a] = self[b][node] + self[node][a]
                self[b].pop(node)
            self.pop(node)

    def dijkstra(self, start, targets, all_paths=False, full_paths=False):
        # find the shortest path from start to targets
        # if multiple paths are tied for shortest, return them all
        # targets must be an iterable, preferably a set, even if it's just one target
        # if all_paths, return paths to all points in graph, else only paths with min weight
        # if full_paths, return tuple of points in path, else return just the path weight
        if not isinstance(targets, set):
            targets = set(targets)
        assert len(targets & self.keys()) > 0, 'Target(s) not in graph'
        q = BFSQ(start)
        parents = {}
        for curr_loc, curr_weight in q:
            if curr_loc not in self:
                continue
            if curr_loc in targets:
                if not all_paths:
                    break
                if q.closed.keys() & targets == targets:
                    break
            for new_loc, new_weight in self[curr_loc].items():
                new_weight = curr_weight + new_weight
                if q.add(new_loc, new_weight):
                    parents[new_loc] = curr_loc
        solutions = {key: val for key, val in q.closed.items() if key in targets}
        if full_paths:
            paths = {}
            for loc, dist in solutions.items():
                path = [loc]
                while loc in parents:
                    loc = parents[loc]
                    path.append(loc)
                paths[tuple(reversed(path))] = dist
            return paths
        else:
            return solutions

    def simple_dijkstra(self, start, end):
        return self.dijkstra(start, {end})[end]

    def copy(self):
        copy = Graph(self.default)
        for node, neighbors in self.items():
            copy[node] = neighbors.copy()
        return copy


def text_to_dict(text, exclude=None, include=None, transpose=False, yinv=False):
    if exclude is None:
        exclude = set()
    else:
        exclude = {i for i in exclude}
    ret = {spatial.Point(x, y): c for y, line in enumerate(text.split('\n')) for x, c in enumerate(line) if c not in exclude}
    if include is not None:
        include = {i for i in include}
        ret = {key: val for key, val in ret.items() if val in include}
    if yinv is True:
        ret = {point.yinv(): c for point, c in ret.items()}
    if transpose is True:
        ret = {point.transpose(): c for point, c in ret.items()}
    return ret


def set_to_graph(map_set, diagonals=False):
    if diagonals is True:
        directions = spatial.ENWS8
    else:
        directions = spatial.ENWS
    ret = Graph()
    map_set = set(map_set)
    for point in map_set:
        for d in directions:
            n = point + d
            if n in map_set:
                ret.add_edge_eq(point, n)
    return ret


def poi_graph(base_graph, poi):
    ret = Graph()
    poi_inv = {val: key for key, val in poi.items()}
    for key, val in poi.items():
        targets = set(poi.values()) - {val}
        paths = base_graph.dijkstra(val, targets, all_paths=True)
        for loc, dist in paths.items():
            key2 = poi_inv[loc]
            ret.add_edge_eq(key, key2, dist)
    return ret
