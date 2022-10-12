import dancer
from common import graph, constants as con, elementwise as ew
from itertools import combinations, permutations


def neighbors(duct_graph, node):
    adjacent = {ew.sum2d(node, direction) for direction in con.D2D4} & duct_graph.graph.keys()
    return {node: 1 for node in adjacent}


def main(input_string, verbose=False):
    duct_graph = graph.Graph()
    wire_graph = graph.Graph()
    wires = {}
    for y, line in enumerate(input_string.split('\n')):
        for x, c in enumerate(line):
            point = (x, y)
            if c == '.':
                duct_graph.add_node(point)
            elif c.isdigit():
                duct_graph.add_node(point)
                wires[c] = point
                wire_graph.add_node(c)
    duct_graph.make_edges(neighbors)
    for a, b in combinations(wire_graph.graph.keys(), 2):
        aloc = wires[a]
        bloc = wires[b]
        weight, _ = duct_graph.dijkstra(aloc, (bloc,))
        wire_graph.add_edge_eq(a, b, weight)
    home = '0'
    to_visit = set(wire_graph.graph.keys()) - {home}
    p1, p2 = None, None
    for route in permutations(to_visit):
        p1len = sum(wire_graph.graph[a][b] for a, b in zip((home,) + route, route))
        if p1 is None or p1len < p1:
            p1 = p1len
        p2len = sum(wire_graph.graph[a][b] for a, b in zip((home,) + route, route + (home,)))
        if p2 is None or p2len < p2:
            p2 = p2len
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2016, day=24, verbose=True)
