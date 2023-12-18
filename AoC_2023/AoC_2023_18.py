import dancer
from common import spatial
from collections import defaultdict
from itertools import product


def intersection_length(cranges, nranges):
    il = 0
    for (ca, cb), (na, nb) in product(cranges, nranges):
        ia = max(ca, na)
        ib = min(cb, nb)
        if ib >= ia:
            il += (ib - ia + 1)
    return il


def dig(instructions):
    digger = spatial.Point(0, 0)
    lines = defaultdict(set)
    for direction, distance in instructions:
        digger += direction * distance
        lines[digger.y].add(digger.x)
    return fill(lines)


def fill(lines):
    full = 0
    current, cranges = set(), tuple()
    csum, cy = 0, min(lines)-1
    for y in sorted(lines):
        full += csum * (y - cy + 1)
        new = current ^ lines[y]
        nsort = sorted(new)
        nranges = tuple((a, b) for a, b in zip(nsort[::2], nsort[1::2]))
        full -= intersection_length(cranges, nranges)
        csum = sum((b-a+1) for a, b in nranges)
        current, cranges, cy = new, nranges, y
    return full


def main(input_string, verbose=False):
    p1_instructions = []
    p2_instructions = []
    directions = (spatial.EAST, spatial.SOUTH, spatial.WEST, spatial.NORTH)
    letters = 'RDLU'
    ddict = {a: b for a, b in zip(letters, directions)}
    for line in input_string.split('\n'):
        direction, distance, hexcode = line.split()
        direction = ddict[direction]
        p1_instructions.append((direction, int(distance)))
        direction = directions[int(hexcode[-2])]
        distance = int(hexcode[2:-2], 16)
        p2_instructions.append((direction, distance))
    p1 = dig(p1_instructions)
    p2 = dig(p2_instructions)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2023, day=18, verbose=True)
