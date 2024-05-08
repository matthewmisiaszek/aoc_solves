import blitzen
from donner import spatial as sp


def santa(instructions):
    pos = sp.Point()
    houses = {pos}
    for c in instructions:
        pos += sp.NAMES_2D[c]
        houses.add(pos)
    return houses


@blitzen.run
def main(input_string, verbose=False):
    p1 = len(santa(input_string))
    p2 = len(santa(input_string[::2]) | santa(input_string[1::2]))
    return p1, p2

