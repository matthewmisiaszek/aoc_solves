import dancer
from common import constants as con, elementwise as ew


def santa(instructions):
    pos = con.origin2
    houses = {pos}
    for c in instructions:
        pos = ew.sum2d(pos, con.caret[c])
        houses.add(pos)
    return houses


def main(input_string, verbose=False):
    p1 = len(santa(input_string))
    p2 = len(santa(input_string[::2]) | santa(input_string[1::2]))
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2015, day=3, verbose=True)
