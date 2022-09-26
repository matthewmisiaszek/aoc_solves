import core
from common import printer


def fold(foldstr, grid):
    axis, n = foldstr.split()[2].split('=')
    n = int(n)
    axis = 'xy'.find(axis)
    for key in tuple(grid):
        if key[axis] > n:
            grid.discard(key)
            key = ((2 * n - key[0]) * (1 - axis) + key[0] * axis, (2 * n - key[1]) * axis + key[1] * (1 - axis))
            grid.add(key)


def makegrid(points):
    grid = set()
    points = points.split('\n')
    for point in points:
        x, y = (int(i) for i in point.split(','))
        grid.add((x, y))
    return grid


def printgrid(grid):
    minbound = [min(grid, key=lambda x: x[i])[i] for i in (0, 1)]
    maxbound = [max(grid, key=lambda x: x[i])[i] for i in (0, 1)]
    ret = ''
    for y in range(minbound[1], maxbound[1] + 1):
        for x in range(minbound[0], maxbound[0] + 1):
            if (x, y) in grid:
                ret += '#'
            else:
                ret += ' '
        ret += '\n'
    return ret


def main(input_string, verbose=False):
    points, folds = input_string.split('\n\n')
    grid = makegrid(points)
    folds = folds.split('\n')
    fold(folds.pop(0), grid)
    p1 = len(grid)
    for foldi in folds:
        fold(foldi, grid)
    p2 = printer.strset(grid)#printgrid(grid)

    return p1, p2


if __name__ == "__main__":
    core.run(main, year=2021, day=13, verbose=True)
