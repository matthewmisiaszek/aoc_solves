import sys
sys.path.append('..')
from common.aoc_input import aoc_input


def neighbors(p):
    return ((p[0] + o[0], p[1] + o[1]) for o in ((-1, 0), (0, -1), (1, 0), (0, 1)))


def main(input_string, verbose=False):
    f = input_string.split('\n')
    pointlist = [(x, y) for x in range(len(f[0])) for y in range(len(f)) if f[y][x] != '9']
    pointlist.sort(key=lambda x: f[x[1]][x[0]])
    pointset = set(pointlist)
    basins = []
    risk = 0
    while pointlist:
        point = pointlist.pop(0)
        if point in pointset:
            q, len_before = [point], len(pointset)
            pointset.discard(point)
            risk += int(f[point[1]][point[0]]) + 1
            while q:
                for n in neighbors(q.pop(0)):
                    if n in pointset:
                        q.append(n)
                        pointset.discard(n)
            basins.append(len_before - len(pointset))
    p1 = risk
    basins.sort()
    p2 = 1
    for basin in basins[-3:]:
        p2 *= basin

    if verbose:
        print('Part 1: {0[0]}\nPart 2: {0[1]}'.format([p1, p2]))
    return p1, p2


if __name__ == "__main__":
    main(aoc_input(2021, 9), verbose=True)
