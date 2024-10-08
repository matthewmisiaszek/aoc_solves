import blitzen
from donner import graph, spatial
from donner.bfsqueue import BFSQ
from numba import njit
from numba.typed import Dict


def numbagraph(pythongraph):
    ret = Dict()
    for node in pythongraph:
        neighbors = Dict()
        for neighbor, weight in pythongraph[node].items():
            neighbors[neighbor] = weight
        ret[node] = neighbors
    return ret


def find_longest(trailmap, slopes=False):
    trailgraph = graph.set_to_graph(trailmap.keys())
    if slopes:
        for node, c in trailmap.items():
            if c in spatial.NAMES_2D:
                trailgraph[node] = {node + spatial.NAMES_2D[c]: 1}
    trailgraph.contract()
    start = min(trailgraph)
    target = max(trailgraph)
    sn = {k: i for i, k in enumerate(trailgraph)}  # replace points with faster integer node names
    trailgraph = {sn[k]: {sn[j]: d for j, d in kg.items()} for k, kg in trailgraph.items()}
    # trailgraph.clear()
    # trailgraph.update(ntg)
    start = sn[start]
    target = sn[target]

    # trace the trail of 3 edge nodes around the perimeter
    # prune the edge pointing back towards start along the perimeter
    # any path that goes from start to the perimeter and then back towards start will be unable to reach target
    q = BFSQ(start)
    for node, weight in q:
        for neighbor in trailgraph[node]:
            connections = trailgraph[neighbor]
            if len(connections) == 3 and node in connections:
                connections.pop(node)
            q.add(neighbor, weight + 1)
    return find_longest_rec(numbagraph(trailgraph), start, target, 0, {-1})


@njit
def find_longest_rec(trailgraph, current, target, weight, visited):
    if current == target:
        return weight
    visited.add(current)
    maxlen = 0
    for neighbor, nweight in trailgraph[current].items():
        if neighbor in visited:
            continue
        maxlen = max(maxlen, find_longest_rec(trailgraph, neighbor, target, weight + nweight, visited))
    visited.discard(current)
    return maxlen


@blitzen.run
def main(input_string, verbose=False):
    trailmap = graph.text_to_dict(input_string, exclude='#')
    p1 = find_longest(trailmap, slopes=True)
    p2 = find_longest(trailmap, slopes=False)
    return p1, p2
