from common2020 import aoc_input
from common.timer import timer
from common.common import CRT


def main(input_string, verbose=False):
    earliest, ids = input_string.split('\n')
    ids = [(int(bus), -i) for i, bus in enumerate(ids.split(',')) if bus.isdigit()]
    earliest = int(earliest)
    wait, best_bus = min([(bus - earliest % bus, bus) for bus, _ in ids])
    p1 = wait * best_bus
    p2 = CRT(*zip(*ids))
    if verbose:
        print('Part 1: {0[0]}\nPart 2: {0[1]}'.format([p1, p2]))
    return p1, p2


if __name__ == "__main__":
    main(aoc_input(2020, 13), verbose=True)
    print('Time:  ', timer())
