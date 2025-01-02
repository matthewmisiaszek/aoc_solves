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
            diff = (a - b) // d
            for p1lim, diff in ((1, diff), (2, diff * -1)):
                point = a
                for i in range(size):
                    if not spatial.inbounds(point, bounds):
                        break
                    if i == p1lim:
                        p1.add(point)
                    p2.add(point)
                    point += diff
    p1 = len(p1)
    p2 = len(p2)
    return p1, p2

