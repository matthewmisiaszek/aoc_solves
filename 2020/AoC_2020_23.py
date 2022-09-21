from common2020 import aoc_input
from common.timer import timer


def get_next(cups, cup):
    if cup in cups:
        return cups[cup]
    else:
        return cup + 1


def crab_cups(cups_in, max_cup, moves, n_return=None):
    cups = {}
    for i in range(len(cups_in) - 1):
        cups[cups_in[i]] = cups_in[i + 1]
    if max_cup > len(cups_in):
        cups[cups_in[-1]] = len(cups_in) + 1
        cups[max_cup] = cups_in[0]
    else:
        cups[cups_in[-1]] = cups_in[0]
    current = cups_in[0]
    for _ in range(moves):
        cup1 = get_next(cups, current)
        cup2 = get_next(cups, cup1)
        cup3 = get_next(cups, cup2)
        new_current = get_next(cups, cup3)
        cups[current] = new_current
        destination = current
        while destination in {current, cup1, cup2, cup3}:
            destination -= 1
            if destination <= 0:
                destination = max_cup
        cups[cup3] = get_next(cups, destination)
        cups[destination] = cup1
        current = new_current
    current = 1
    ret = []
    if n_return is None:
        n_return = len(cups_in)
    for _ in range(n_return):
        current = get_next(cups, current)
        ret.append(current)
    return ret


def main(input_string, verbose=False):
    cups = tuple(int(i) for i in input_string)
    p1cups = crab_cups(cups, 9, 100)
    p1 = ''.join((str(i) for i in p1cups[:-1]))
    p2cups = crab_cups(cups, 10 ** 6, 10 ** 7, 2)
    p2 = p2cups[0] * p2cups[1]
    if verbose:
        print('Part 1: {0[0]}\nPart 2: {0[1]}'.format([p1, p2]))
    return p1, p2


if __name__ == "__main__":
    main(aoc_input(2020, 23), verbose=True)
    print('Time:  ', timer())
