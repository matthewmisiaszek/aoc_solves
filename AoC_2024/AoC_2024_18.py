import blitzen
from donner import spatial, graph


@blitzen.run
def main(input_string, verbose=False):
    bounds = spatial.Point(70, 70)
    memory_space = graph.set_to_graph({spatial.Point(x, y) for x in range(bounds.x + 1) for y in range(bounds.y + 1)})
    path = ()
    for i, line in enumerate(input_string.split('\n')):
        n = spatial.Point(*(int(i) for i in line.split(',')))
        memory_space.rem_node(n)
        if not path or n in path:
            start, target = spatial.bounds(memory_space)
            paths = memory_space.dijkstra(start, {target}, full_paths=True)
            for path, plen in paths.items():
                if path[-1] == target:
                    break
            else:
                break
        if i == 1024 - 1:
            p1 = plen
    p2 = line
    return p1, p2
