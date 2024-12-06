import blitzen
from donner import graph, spatial
import multiprocessing


def part1(bounds, obstacles, guard, heading):
    visited = set()
    while spatial.inbounds(guard, bounds):
        if guard in obstacles:
            guard -= heading
            heading = heading.right()
        visited.add(guard)
        guard += heading
    return visited


def part2(bounds, obstacles, guard, heading):
    visited = set()
    while spatial.inbounds(guard, bounds):
        if guard in obstacles:
            guard -= heading
            heading = heading.right()
        if (guard, heading) in visited:
            return True
        visited.add((guard, heading))
        guard += heading
    return False


@blitzen.run
def main(input_string, verbose=False):
    grid = graph.text_to_dict(input_string)
    bounds = spatial.bounds(grid)
    obstacles = {point for point, c in grid.items() if c == '#'}
    for point, c in grid.items():
        if c in spatial.NAMES_2D:
            guard = point
            heading = spatial.NAMES_2D[c]
            break
    p1visited = part1(bounds, obstacles, guard, heading)
    p1 = len(p1visited)
    with multiprocessing.Pool(8) as pool:
        iterable = tuple((bounds, obstacles | {i}, guard, heading) for i in p1visited)
        p2 = sum(pool.starmap_async(part2, iterable).get())
    return p1, p2
