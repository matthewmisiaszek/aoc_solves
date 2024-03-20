import dancer
from common import graph, spatial
from common.bfsqueue import BFSQ


def find_longest(trailmap, slopes=False):
    trailgraph = graph.set_to_graph(trailmap.keys())
    if slopes:
        for node, c in trailmap.items():
            if c in spatial.NAMES_2D:
                trailgraph[node] = {node + spatial.NAMES_2D[c]: 1}
    trailgraph.contract()
    start = min(trailgraph)
    target = max(trailgraph)
    # trace the trail of 3 edge nodes around the perimeter
    # prune the edge pointing back towards start along the perimeter
    # any path that goes from start to the perimeter and then back towards start will be unable to reach target
    q = BFSQ(start)
    for node, weight in q:
        for neighbor in trailgraph[node]:
            connections = trailgraph[neighbor]
            if len(connections) != 3:
                continue
            if node in connections:
                connections.pop(node)
            q.add(neighbor, 0)
    return find_longest_rec(trailgraph, start, target, 0, set())


def find_longest_rec(trailgraph, current, target, weight, visited):
    if current == target:
        return weight
    visited.add(current)
    maxlen = weight
    for neighbor, nweight in trailgraph[current].items():
        if neighbor in visited:
            continue
        maxlen = max(maxlen, find_longest_rec(trailgraph, neighbor, target, weight + nweight, visited))
    visited.discard(current)
    return maxlen


def main(input_string, verbose=False):
    trailmap = graph.text_to_dict(input_string, exclude='#')
    p1 = find_longest(trailmap, slopes=True)
    p2 = find_longest(trailmap, slopes=False)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2023, day=23, verbose=True)
