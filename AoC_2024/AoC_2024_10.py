import blitzen
from donner import spatial, graph


def dfs(tgraph, point, nines, trail=()):
    if point in nines:
        return 1
    ret = 0
    for n in tgraph[point]:
        if n not in trail:
            ret += dfs(tgraph, n, nines, trail + (n,))
    return ret


@blitzen.run
def main(input_string, verbose=False):
    topodict = graph.text_to_dict(input_string, exclude='.')
    topodict = {point: int(val) for point, val in topodict.items()}
    zeros, nines = ({point for point, val in topodict.items() if val == i} for i in (0, 9))
    topograph = graph.Graph()
    for point in topodict:
        topograph.add_node(point)
        for d in spatial.ENWS:
            if point + d in topodict and topodict[point] + 1 == topodict[point + d]:
                topograph.add_edge_neq(point, point+d)
    p1 = sum(len(topograph.dijkstra(point, nines, all_paths=True)) for point in zeros)
    p2 = sum(dfs(topograph, point, nines) for point in zeros)
    return p1, p2

