import blitzen
from donner import graph, bfsqueue


def unique_paths(near, target, wm):
    deletions = set()
    ret = False
    for paths in range(4):
        for used in wm.dijkstra(near, {target}, full_paths=True):
            for a, b in zip(used, used[1:]):
                wm[a].pop(b)
                wm[b].pop(a)
                deletions.add((a, b))
            break
        else:
            break
    else:
        ret = True
    for a, b in deletions:
        wm.add_edge_eq(a, b)
    return ret


def parse(input_string):
    weather_machine = graph.Graph()
    for line in input_string.split('\n'):
        node, neighbors = line.split(': ')
        for neighbor in neighbors.split(' '):
            weather_machine.add_edge_eq(node, neighbor)
    return weather_machine, node


def trim_far_nodes(weather_machine, node):
    near = {node}
    q = bfsqueue.BFSQ(node)
    for node, dist in q:
        if not unique_paths(near, node, weather_machine):
            continue
        near.add(node)
        for neighbor in weather_machine[node]:
            q.add(neighbor, dist + 1)
    return (len(weather_machine) - len(near)) * len(near)


@blitzen.run
def main(input_string, verbose=False):
    weather_machine, node = parse(input_string)
    p1 = trim_far_nodes(weather_machine, node)
    p2 = blitzen.holiday_greeting
    return p1, p2

