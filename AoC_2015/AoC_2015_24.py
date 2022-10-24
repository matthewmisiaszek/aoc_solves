import dancer
from itertools import combinations
from common import elementwise as ew


def balance(packages, n_groups):
    goal_weight = sum(packages) / n_groups
    for n in range(1, len(packages) + 1):
        small_groups = [group for group in combinations(packages, n) if sum(group) == goal_weight]
        if small_groups:
            small_groups.sort(key=lambda x: ew.prod(x))
            for group in small_groups:
                if n_groups == 2 or balance(packages - set(group), n_groups - 1) is not False:
                    return ew.prod(group)
    return False


def main(input_string, verbose=False):
    packages = {int(i) for i in input_string.split('\n')}
    p1 = balance(packages, 3)
    p2 = balance(packages, 4)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2015, day=24, verbose=True)
