from common2020 import aoc_input
from common.timer import timer
from common.elementwise import prod


def check_slope(trees, slope, bottom, width):
    tx, ty = 0, 0
    sx, sy = slope
    tree_count = 0
    while ty <= bottom:
        tree_count += (tx, ty) in trees
        tx, ty = (tx + sx) % width, ty + sy
    return tree_count


def parse(input_string):
    tree = '#'
    trees = {(x, y)
             for y, line in enumerate(input_string.split('\n'))
             for x, c in enumerate(line)
             if c is tree}
    bottom = input_string.count('\n')
    width = input_string.find('\n')
    return trees, bottom, width


def main(input_string, verbose=False):
    trees, bottom, width = parse(input_string)
    slopes = ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))
    tree_counts = {slope: check_slope(trees, slope, bottom, width) for slope in slopes}
    p1 = tree_counts[(3, 1)]
    p2 = prod(tree_counts.values())
    if verbose:
        print('Part 1: {0[0]}\nPart 2: {0[1]}'.format([p1, p2]))
    return p1, p2


if __name__ == "__main__":
    main(aoc_input(2020, 3), verbose=True)
    print('Time:  ', timer())
