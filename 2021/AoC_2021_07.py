import sys
sys.path.append('..')
from common.aoc_input import aoc_input
import statistics


def main(input_string, verbose=False):
    crabs = [int(i) for i in input_string.split(',')]
    crabs.sort()
    median, average = int(statistics.median(crabs)), int(statistics.mean(crabs))
    p1 = sum([abs(crab - median) for crab in crabs])
    p2 = min([sum([sum(range(abs(crab - average) + 1)) for crab in crabs]) for average in [average, average + 1]])
    if verbose:
        print('Part 1: {0[0]}\nPart 2: {0[1]}'.format([p1, p2]))
    return p1, p2


if __name__ == "__main__":
    main(aoc_input(2021, 7), verbose=True)
