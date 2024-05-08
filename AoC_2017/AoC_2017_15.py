import blitzen
from numba import njit


@njit
def generator(value, factor, modulus, judge_modulus):
    while True:
        value *= factor
        value %= modulus
        yield value & judge_modulus


@njit
def picky_generator(value, factor, modulus, judge_modulus, picky_modulus):
    while True:
        value *= factor
        value %= modulus
        if value % picky_modulus == 0:
            yield value & judge_modulus


@njit
def solve(value_a, value_b):
    a = generator(value=value_a, factor=16807, modulus=2147483647, judge_modulus=0xffff)
    b = generator(value=value_b, factor=48271, modulus=2147483647, judge_modulus=0xffff)
    p1 = p2 = 0
    for _ in range(40 * 10 ** 6):
        p1 += next(a) == next(b)
    a = picky_generator(value=value_a, factor=16807, modulus=2147483647, judge_modulus=0xffff, picky_modulus=4)
    b = picky_generator(value=value_b, factor=48271, modulus=2147483647, judge_modulus=0xffff, picky_modulus=8)
    for _ in range(5 * 10 ** 6):
        p2 += next(a) == next(b)
    return p1, p2


@blitzen.run
def main(input_string, verbose=False):
    value_a, value_b = [int(i) for i in (line.split()[-1] for line in input_string.split('\n'))]
    return solve(value_a, value_b)

