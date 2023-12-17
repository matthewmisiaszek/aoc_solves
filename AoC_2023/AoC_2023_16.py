import dancer
from common import graph, spatial as sp
from collections import defaultdict


START = sp.Point(-1, 0)
GLASS = {
    '\\': {
        sp.NORTH: (sp.WEST,),
        sp.EAST: (sp.SOUTH,),
        sp.SOUTH: (sp.EAST,),
        sp.WEST: (sp.NORTH,),
    },
    '/': {
        sp.NORTH: (sp.EAST,),
        sp.EAST: (sp.NORTH,),
        sp.SOUTH: (sp.WEST,),
        sp.WEST: (sp.SOUTH,),
    },
    '-': {
        sp.NORTH: (sp.WEST, sp.EAST),
        sp.SOUTH: (sp.WEST, sp.EAST),
    },
    '|': {
        sp.EAST: (sp.NORTH, sp.SOUTH),
        sp.WEST: (sp.NORTH, sp.SOUTH),
    },
}


def energize(grid, start, startdir):
    energized = defaultdict(set)
    beams = {(start, startdir)}
    bounds = sp.bounds(grid)
    while beams:
        point, direction = beams.pop()
        if point in energized and direction in energized[point]:
            continue
        while sp.inbounds(point, bounds) or point == start:
            energized[point].add(direction)
            point += direction
            if point in grid and direction in GLASS[grid[point]]:
                for direction2 in GLASS[grid[point]][direction]:
                    beams.add((point, direction2))
                break
    energized.pop(start)
    return len(energized)


def main(input_string, verbose=False):
    grid = graph.text_to_dict(input_string, include=GLASS.keys())
    p1 = energize(grid, sp.Point(-1, 0), sp.EAST)
    bn, bx = sp.bounds(grid)
    p2 = 0
    for x in range(bn.x, bx.x):
        p2 = max(p2, energize(grid, sp.Point(x, bn.y-1), sp.SOUTH))
        p2 = max(p2, energize(grid, sp.Point(x, bx.y), sp.NORTH))
    for y in range(bn.y, bx.y):
        p2 = max(p2, energize(grid, sp.Point(bn.x-1, y), sp.EAST))
        p2 = max(p2, energize(grid, sp.Point(bx.x, y), sp.WEST))
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2023, day=16, verbose=True)
