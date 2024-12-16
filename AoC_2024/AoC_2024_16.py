import blitzen
from donner import graph, spatial, bfsqueue, printer
from itertools import product
from collections import defaultdict


def parse(input_string):
    maze = graph.text_to_dict(input_string, exclude='#')
    rmaze = {v: k for k, v in maze.items()}
    startpt, endpt = (rmaze[i] for i in 'SE')
    maze_graph = graph.Graph()
    for point, direction in product(maze.keys(), spatial.ENWS):
        neighbor = (point + direction, direction)
        if point + direction in maze:
            maze_graph.add_edge_neq((point, direction), neighbor, 1)
            maze_graph.add_edge_neq((point, direction.right()), neighbor, 1001)
            maze_graph.add_edge_neq((point, direction.left()), neighbor, 1001)
    start = (startpt, spatial.EAST)
    target = {(endpt, d) for d in spatial.ENWS}
    return start, target, maze, maze_graph


@blitzen.run
def main(input_string, verbose=False):
    start, target, maze, maze_graph = parse(input_string)
    node_histories = defaultdict(set)
    p1 = 1000 * len(maze)
    q = bfsqueue.BFSQ(start)
    for node, weight in q:
        if weight > p1:
            continue
        history = node_histories[(node, weight)]
        history.add(node)
        if node in target:
            p1 = weight
            continue
        for neighbor, nweight in maze_graph[node].items():
            node_histories[(neighbor, weight + nweight)].update(history)
            q.add(neighbor, weight + nweight)
    good_seats = set()
    for node in target:
        for seat, _ in node_histories[(node, p1)]:
            good_seats.add(seat)
    p2 = len(good_seats)
    if verbose:
        toprint = maze.copy()
        toprint.update({s: 'O' for s in good_seats})
        printer.printdict(toprint)
    return p1, p2
