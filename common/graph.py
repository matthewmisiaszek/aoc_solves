import dancer
from common import elementwise as ew, constants as con
from common.bfsqueue import BFSQ


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
        self.graph[a].update({b: weight})
        self.graph[b].update({a: weight})

    def add_edge_neq(self, a, b, weight=1):
        for node in (a, b):
            if node not in self.graph:
                self.graph[node] = self.default()
        self.graph[a].update({b: weight})

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
        q = BFSQ(start)
        parents = {}
        for curr_loc, curr_weight in q:
            if curr_loc in targets:
                if not all_paths:
                    break
                if q.closed.keys() & targets == targets:
                    break
            for new_loc, new_weight in self.graph[curr_loc].items():
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


def text_to_dict(text, exclude=None, include=None, transpose=False, yinv=False):
    if exclude is None:
        exclude = set()
    else:
        exclude = {i for i in exclude}
    ret = {(x, y): c for y, line in enumerate(text.split('\n')) for x, c in enumerate(line) if c not in exclude}
    if include is not None:
        include = {i for i in include}
        ret = {key: val for key, val in ret.items() if val in include}
    if yinv is True:
        ret = {(x, -y): c for (x, y), c in ret.items()}
    if transpose is True:
        ret = {(y, x): c for (x, y), c in ret.items()}
    return ret


def set_to_graph(map_set, diagonals=False):
    ret = Graph()
    if diagonals is True:
        directions = con.D2D8
    else:
        directions = con.D2D4
    map_set = set(map_set)
    for point in map_set:
        for d in directions:
            neighbor = ew.sum2d(point, d)
            if neighbor in map_set:
                ret.add_edge_eq(point, neighbor)
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
