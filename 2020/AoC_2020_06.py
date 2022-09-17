from common2020 import aoc_input
from common.timer import timer
from string import ascii_lowercase


def main(input_string, verbose=False):
    p1, p2 = 0, 0
    for group in input_string.split('\n\n'):
        members = group.count('\n') + 1
        for c in ascii_lowercase:
            count = group.count(c)
            p1 += count > 0
            p2 += count == members
    if verbose:
        print('Part 1: {0[0]}\nPart 2: {0[1]}'.format([p1, p2]))
    return p1, p2


if __name__ == "__main__":
    main(aoc_input(2020, 6), verbose=True)
    print('Time:  ', timer())
