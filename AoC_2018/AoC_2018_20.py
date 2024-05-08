import blitzen
from donner import graph, spatial as sp


def re_path(input_string):
    door_graph = graph.Graph()
    directions = sp.NAMES_2D
    f = input_string.strip()
    origin = sp.Point()
    start = {origin}
    current = start.copy()
    end = set()
    stack = []
    for c in f[1:]:
        if c == '(':
            stack.append((start, end))
            start = current.copy()
            end = set()
        elif c == ')':
            current |= end
            start, end = stack.pop()
        elif c == '|':
            end |= current
            current = start.copy()
        elif c in directions:
            direction = directions[c]
            new_current = set()
            for room in current:
                new_room = room + direction
                door_graph.add_edge_eq(room, new_room)
                new_current.add(new_room)
            current = new_current
    return door_graph


@blitzen.run
def main(input_string, verbose=False):
    doors = re_path(input_string)
    paths = doors.dijkstra(sp.Point(0, 0), doors.graph.keys(), all_paths=True)
    p1 = max(paths.values())
    target_length = 1000
    p2 = sum([value >= target_length for value in paths.values()])
    return p1, p2

