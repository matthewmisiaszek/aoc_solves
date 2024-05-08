import blitzen
import re
from itertools import combinations, product


def check_state(state):
    # find all floors with orphaned chips
    # find all floors with generators
    # if these two overlap, the state is invalid!
    orphaned = set()
    has_gen = set()
    for chip, gen in state:
        if chip != gen:
            orphaned.add(chip)
        has_gen.add(gen)
    return not bool(orphaned & has_gen)


def parse(input_string):
    # return a sorted tuple of (chip floor, generator floor) tuple pairs
    # pairs are interchangeable so by sorting them we make equivalent states equal!
    floor_names = ('first', 'second', 'third', 'fourth')
    floor_pattern = 'The (.*) floor contains (.*).'
    obj_pattern = r'an? ([a-z\- ]*)'
    gen_suffix = ' generator'
    chip_suffix = '-compatible microchip'
    pairs = {}
    top_floor = 0
    for floor_name, objects in re.findall(floor_pattern, input_string):
        floor = floor_names.index(floor_name)
        top_floor = max(top_floor, floor)
        for gen in re.findall(obj_pattern + gen_suffix, objects):
            if gen not in pairs:
                pairs[gen] = [0, 0]
            pairs[gen][1] = floor
        for chip in re.findall(obj_pattern + chip_suffix, objects):
            if chip not in pairs:
                pairs[chip] = [0, 0]
            pairs[chip][0] = floor
    state = [tuple(pair) for pair in pairs.values()]
    state = tuple(sorted(state))
    return state, top_floor


def make_moves(queue, steps, elevator, state, top_floor, closed=set()):
    # try all combinations of 1 or 2 items on the current floor and moving up and down
    # if it's valid and not in cache, add to queue
    on_this_floor = {(a, b) for a, pair in enumerate(state) for b, floor in enumerate(pair) if floor == elevator}
    combo1 = list(combinations(on_this_floor, 1))
    combo2 = list(combinations(on_this_floor, 2))
    combos = combo1 + combo2
    directions = [i for i in (-1, 1) if 0 <= elevator + i <= top_floor]
    for direction, moves in product(directions, combos):
        new_elevator = elevator + direction
        new_state = list(state)
        for a, b in moves:
            new_state[a] = list(new_state[a])
            new_state[a][b] += direction
            new_state[a] = tuple(new_state[a])
        new_state = tuple(sorted(new_state))
        closed_key = (new_elevator, new_state)
        if closed_key not in closed:
            closed.add(closed_key)
            if check_state(new_state):
                queue.append((steps + 1, new_elevator, new_state))


def fox_chicken_corn(state, elevator, top_floor):
    # find minimum number of steps to bring all chips and generators to top floor without breaking anything
    target = tuple(tuple(top_floor for _ in group) for group in state)
    queue = [(0, elevator, state)]  # steps, elevator, state
    while queue:
        current = queue.pop(0)
        steps, elevator, state = current
        if state == target:
            return steps
        else:
            make_moves(queue, steps, elevator, state, top_floor)
    return False


@blitzen.run
def main(input_string, verbose=False):
    state, top = parse(input_string)
    p1 = fox_chicken_corn(state, 0, top)
    extra = open(blitzen.root_path+'/AoC_2016/day11_extra_items').read()
    state, top = parse(input_string + '\n' + extra)
    p2 = fox_chicken_corn(state, 0, top)
    return p1, p2

