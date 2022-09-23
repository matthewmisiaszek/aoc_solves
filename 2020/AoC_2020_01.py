import sys
sys.path.append('..')
from common.aoc_input import aoc_input
from common.timer import timer
from common.elementwise import prod
import itertools


def prodifsum(entries, count, target_sum):
    for thing in itertools.combinations(entries, count):
        if sum(thing) == target_sum:
            return prod(thing)
    return False


def main(input_string, verbose=False):
    entries = tuple(sorted(int(i) for i in input_string.split('\n')))
    p1 = prodifsum(entries, 2, 2020)
    p2 = prodifsum(entries, 3, 2020)
    if verbose:
        print('Part 1: {0[0]}\nPart 2: {0[1]}'.format([p1, p2]))
    return p1, p2


if __name__ == "__main__":
    main(aoc_input(2020, 1), verbose=True)
    print('Time:  ', timer())
