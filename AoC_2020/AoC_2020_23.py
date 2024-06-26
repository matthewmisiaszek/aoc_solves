import blitzen


def crab_cups(cups_in, moves, max_cup=None, n_return=None):
    if max_cup is None:
        max_cup = len(cups_in)
    cups = [i + 1 for i in range(max_cup + 1)]
    cups[-1] = cups_in[0]
    for i in range(len(cups_in) - 1):
        cups[cups_in[i]] = cups_in[i + 1]
    if max_cup > len(cups_in):
        cups[cups_in[-1]] = len(cups_in) + 1
    current = cups_in[0]
    for _ in range(moves):
        cup1 = cups[current]
        cup2 = cups[cup1]
        cup3 = cups[cup2]
        new_current = cups[cup3]
        cups[current] = new_current
        destination = current
        while destination in {current, cup1, cup2, cup3}:
            destination -= 1
            if destination <= 0:
                destination = max_cup
        cups[cup3] = cups[destination]
        cups[destination] = cup1
        current = new_current
    current = 1
    ret = []
    if n_return is None:
        n_return = len(cups_in)
    for _ in range(n_return):
        current = cups[current]
        ret.append(current)
    return ret


@blitzen.run
def main(input_string, verbose=False):
    cups = tuple(int(i) for i in input_string)
    p1cups = crab_cups(cups, 100)
    p1 = ''.join((str(i) for i in p1cups[:-1]))
    p2cups = crab_cups(cups, 10 ** 7, 10 ** 6, 2)
    p2 = p2cups[0] * p2cups[1]
    return p1, p2

