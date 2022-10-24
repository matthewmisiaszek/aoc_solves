import dancer
from itertools import combinations as combos


def main(input_string, verbose=False):
    NOG = 150
    containers = [int(i) for i in input_string.split('\n')]
    all_combos = [[sum(combo) for combo in combos(containers, n)] for n in range(1, len(containers) + 1)]
    valid_combos = [[combo for combo in ncombos if combo == NOG] for ncombos in all_combos]
    valid_combos = [ncombos for ncombos in valid_combos if ncombos]  # remove empty lists
    p1 = sum(len(c) for c in valid_combos)
    p2 = len(valid_combos[0])
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2015, day=17, verbose=True)
