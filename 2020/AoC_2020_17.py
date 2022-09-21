from common2020 import aoc_input
from common.timer import timer
from common import cartnd
from itertools import product


def startup(initial_state, order):
    cycles = 6
    stay_active = {2, 3}
    become_active = {3}
    pocket = cartnd.Cart(order)
    coord_tail = (0, ) * (order - 2)
    active = {cube + coord_tail for cube in initial_state}
    for cycle in range(cycles):
        deactivate = set()
        activate = set()
        bounds = cartnd.bounds(active, pocket.order)
        axes = [set(range(n-1, x+2)) for n, x in bounds]
        for cube in product(*axes):
            active_neighbors = len(pocket.adj(cube, pocket.order) & active)
            if cube in active:
                if active_neighbors not in stay_active:
                    deactivate.add(cube)
            elif active_neighbors in become_active:
                activate.add(cube)
        active.difference_update(deactivate)
        active.update(activate)
    return len(active)


def main(input_string, verbose=False):
    active = '#'
    initial_state = {(x, y)
                     for y, line in enumerate(input_string.split('\n'))
                     for x, c in enumerate(line)
                     if c is active}
    p1 = startup(initial_state, 3)
    p2 = startup(initial_state, 4)
    if verbose:
        print('Part 1: {0[0]}\nPart 2: {0[1]}'.format([p1, p2]))
    return p1, p2


if __name__ == "__main__":
    main(aoc_input(2020, 17), verbose=True)
    print('Time:  ', timer())
