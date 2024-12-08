import blitzen
from donner import graph, spatial
from itertools import combinations
from collections import defaultdict
from math import gcd


@blitzen.run
def main(input_string, verbose=False):
    grid = graph.text_to_dict(input_string)
    nodes = defaultdict(set)
    for point, freq in grid.items():
        if freq != '.' and freq != '#':
            nodes[freq].add(point)
    bounds = spatial.bounds(grid)
    size = max(bounds[1].x, bounds[1].y)

    p1, p2 = set(), set()
    for antennas in nodes.values():
        for a, b in combinations(antennas, 2):
            d = max(1, gcd((a-b).x, (a-b).y))  # this didn't come up in my input but what if it did?
            for i in range(-size * d, size * d):
                point = a + (a-b) // d * i
                if not spatial.inbounds(point, bounds):
                    continue
                if abs(i) == d:
                    p1.add(point)
                p2.add(point)
    p1 = len(p1)
    p2 = len(p2)
    return p1, p2

