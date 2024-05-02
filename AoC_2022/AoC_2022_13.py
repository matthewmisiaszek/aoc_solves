import blitzen
import json
from functools import cmp_to_key
from math import prod

DIV_PACKETS = '/AoC_2022/divider_packets'


def cmp(a, b):
    if not (a or b):
        # If the lists are the same length and no comparison makes a decision about the order,
        # continue checking the next part of the input.
        return 0
    if not b:
        # If the right list runs out of items first, the inputs are /not/ in the right order.
        return -1
    if not a:
        # If the left list runs out of items first, the inputs are in the right order.
        return 1
    if a and b:
        ai, bi = a[0], b[0]
        if isinstance(ai, int) and isinstance(bi, int):
            # If both values are integers, the lower integer should come first.
            # Otherwise, the inputs are the same integer; continue checking the next part of the input.
            if ai == bi:
                return cmp(a[1:], b[1:])
            return 1 if ai < bi else -1
        # If exactly one value is an integer, convert the integer to a list
        if isinstance(ai, int):
            ai = [ai]
        if isinstance(bi, int):
            bi = [bi]
        # If the lists are the same length and no comparison makes a decision about the order,
        # continue checking the next part of the input.
        x = cmp(ai, bi)
        return x if x != 0 else cmp(a[1:], b[1:])


def part1(input_string):
    p1 = 0
    for idx, pair in enumerate(input_string.split('\n\n')):
        a, b = (json.loads(i) for i in pair.split('\n'))
        if cmp(a, b) == 1:
            p1 += idx + 1
    return p1


def part2(input_string):
    divider_packets_str = open(blitzen.root_path + DIV_PACKETS).read().split('\n')
    div_packets = [json.loads(i) for i in divider_packets_str]
    packets = [json.loads(i) for i in input_string.replace('\n\n', '\n').split('\n')] + div_packets
    packets.sort(key=cmp_to_key(cmp))
    return prod(packets.index(i) for i in div_packets)


def main(input_string, verbose=False):
    p1 = part1(input_string)
    p2 = part2(input_string)
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2022, day=13, verbose=True)
