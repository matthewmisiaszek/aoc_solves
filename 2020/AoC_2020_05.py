import DANCER
from common.misc import digits


def main(input_string, verbose=False):
    ones = {'B', 'R'}
    ids = {digits(tuple(c in ones for c in ticket), 2)
           for ticket in input_string.split('\n')}
    p1 = max(ids)
    empty_seats = set(range(min(ids), max(ids))) - ids
    for p2 in empty_seats:
        if p2 + 1 in ids and p2 - 1 in ids:
            break
    return p1, p2


if __name__ == "__main__":
    DANCER.run(main, year=2020, day=5, verbose=True)
