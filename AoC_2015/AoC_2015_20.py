import blitzen
from numba import njit


@njit
def busywork(presents, target, endurance=None):
    n_houses = target // presents
    if endurance is None:
        endurance = n_houses
    houses = [0] * n_houses
    for i in range(1, n_houses):
        for j in range(i, min(n_houses, i*(endurance+1)), i):
            houses[j] += i * presents
    for i, house in enumerate(houses):
        if house >= target:
            return i


@blitzen.run
def main(input_string, verbose=False):
    target = int(input_string)
    p1 = busywork(10, target)
    p2 = busywork(11, target, 50)
    return p1, p2

