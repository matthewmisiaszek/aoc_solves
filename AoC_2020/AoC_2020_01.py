import dancer
from common.elementwise import prod
import itertools


def prodifsum(entries, count, target_sum):
    for thing in itertools.combinations(entries, count):
        if sum(thing) == target_sum:
            return prod(thing)
    return False


def main(input_string, verbose=False):
    entries = tuple(sorted(int(i) for i in input_string.split('\n')))
    p1 = prodifsum(entries, 2, 2020)
    p2 = prodifsum(entries, 3, 2020)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2020, day=1, verbose=True)
