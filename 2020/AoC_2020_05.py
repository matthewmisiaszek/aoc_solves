from common2020 import aoc_input
from common.timer import timer
from common.common import digits


def main(input_string, verbose=False):
    tickets = tuple((tuple(c == 'B' for c in ticket[:7]),
                     tuple(c == 'R' for c in ticket[7:]))
                    for ticket in input_string.split('\n'))
    ids = {digits(a, 2) * 8 + digits(b, 2) for a, b in tickets}
    p1 = max(ids)
    empty_seats = set(range(min(ids), max(ids))) - ids
    for p2 in empty_seats:
        if p2 + 1 in ids and p2 - 1 in ids:
            break
    if verbose:
        print('Part 1: {0[0]}\nPart 2: {0[1]}'.format((p1, p2)))
    return p1, p2


if __name__ == "__main__":
    main(aoc_input(2020, 5), verbose=True)
    print('Time:  ', timer())