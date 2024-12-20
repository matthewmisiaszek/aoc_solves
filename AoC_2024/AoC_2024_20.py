import blitzen
from donner import graph


@blitzen.run
def main(input_string, verbose=False):
    p1 = p2 = 0
    trackmap = graph.text_to_dict(input_string, exclude='#')
    trackmap_inv = {v: k for k, v in trackmap.items()}
    s = trackmap_inv['S']
    e = trackmap_inv['E']
    trackgraph = graph.set_to_graph(trackmap)
    path = list(trackgraph.dijkstra(s, {e}, full_paths=True))[0]
    for spi, sp in enumerate(path):
        epi = spi + 102
        while epi < len(path):
            ep = path[epi]
            md = ep.manhattan(sp)
            if md > 20:
                epi += md - 20
                continue
            savings = epi - spi - md
            if savings >= 100:
                if md == 2:
                    p1 += 1
                p2 += 1
            epi += 1
    return p1, p2
