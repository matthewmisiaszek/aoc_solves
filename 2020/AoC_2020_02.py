from common2020 import aoc_input
from common.timer import timer
import re


def part1(example_list):
    return sum(a <= password.count(c) <= b
               for a, b, c, password in example_list)


def part2(example_list):
    return sum((a <= len(password) and password[a - 1] == c) ^
               (b <= len(password) and password[b - 1] == c)
               for a, b, c, password in example_list)


def main(input_string, verbose=False):
    pattern = '(.*)-(.*) (.): (.*)'
    example_list = tuple((int(a), int(b), c, d) for a, b, c, d in re.findall(pattern, input_string))
    p1 = part1(example_list)
    p2 = part2(example_list)
    if verbose:
        print('Part 1: {0[0]}\nPart 2: {0[1]}'.format([p1, p2]))
    return p1, p2


if __name__ == "__main__":
    main(aoc_input(2020, 2), verbose=True)
    print('Time:  ', timer())