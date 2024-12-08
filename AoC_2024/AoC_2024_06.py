import blitzen
from donner import graph, spatial


def parse(input_string):
    grid = graph.text_to_dict(input_string)
    bounds = spatial.bounds(grid)
    obstacles = {point for point, c in grid.items() if c == '#'}
    for point, c in grid.items():
        if c in spatial.NAMES_2D:
            guard = point
            heading = spatial.NAMES_2D[c]
            break
    return bounds, obstacles, guard, heading


def check_loops(obstacles, bounds, guard, heading, trail):
    while spatial.inbounds(guard, bounds):
        if (guard, heading) in trail:
            return True
        trail.add((guard, heading))
        while guard + heading in obstacles:
            heading = heading.right()
        guard += heading
    return False


@blitzen.run
def main(input_string, verbose=False):
    bounds, obstacles, guard, heading = parse(input_string)
    p1, p2, trail = set(), set(), set()
    while spatial.inbounds(guard, bounds):
        p1.add(guard)
        while guard + heading in obstacles:
            heading = heading.right()
        new_guard = guard + heading
        if all((
            new_guard not in p1,
            spatial.inbounds(new_guard, bounds),
            check_loops(obstacles | {new_guard}, bounds, guard, heading, trail.copy()),
        )):
            p2.add(new_guard)
        trail.add((guard, heading))
        guard = new_guard
    p1, p2 = len(p1), len(p2)
    return p1, p2
