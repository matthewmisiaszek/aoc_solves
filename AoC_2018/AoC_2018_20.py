import dancer
from common import graph
from common import constants


def re_path(input_string):
    door_graph = graph.Graph()
    directions = constants.NSEW
    f = input_string.strip()
    origin = constants.origin2
    start = {origin}
    current = start.copy()
    end = set()
    stack = []
    for c in f:
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
                new_room = (room[0] + direction[0], room[1] + direction[1])
                door_graph.add_edge_eq(room, new_room)
                new_current.add(new_room)
            current = new_current
    return door_graph


def main(input_string, verbose=False):
    doors = re_path(input_string)
    p1, paths = doors.dijkstra((0, 0), doors.graph.keys(), all_paths=True)
    target_length = 1000
    p2 = sum([value > target_length for value in paths.values()])
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2018, day=20, verbose=True)
