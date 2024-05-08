import blitzen
from itertools import combinations
from math import prod


def balance(packages, n_groups):
    goal_weight = sum(packages) / n_groups
    for n in range(1, len(packages) + 1):
        small_groups = [group for group in combinations(packages, n) if sum(group) == goal_weight]
        if small_groups:
            small_groups.sort(key=lambda x: prod(x))
            for group in small_groups:
                if n_groups == 2 or balance(packages - set(group), n_groups - 1) is not False:
                    return prod(group)
    return False


@blitzen.run
def main(input_string, verbose=False):
    packages = {int(i) for i in input_string.split('\n')}
    p1 = balance(packages, 3)
    p2 = balance(packages, 4)
    return p1, p2

