import blitzen
from donner import graph
from itertools import permutations

WALL = '#'
DUCT = '.'


def main(input_string, verbose=False):
    duct_dict = graph.text_to_dict(input_string, exclude=WALL)
    duct_graph = graph.set_to_graph(duct_dict.keys())
    wires = {val: key for key, val in duct_dict.items()}
    wires.pop(DUCT)
    wire_graph = graph.poi_graph(duct_graph, wires)
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
    blitzen.run(main, year=2016, day=24, verbose=True)
