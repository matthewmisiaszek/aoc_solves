import blitzen
from donner import spatial, graph


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
    p1 = p2 = 0
    for point in zeros:
        visited = set()
        q = [point]
        while q:
            c = q.pop(-1)
            if c in nines:
                p2 += 1
                visited.add(c)
            q.extend(topograph[c].keys())
        p1 += len(visited)
    return p1, p2

