import dancer


class Unit:
    def __init__(self, team):
        self.team = team
        self.hit_points = 200


def parse(input_string):
    # read input file and return units, a map of point:unit and floor, a set of points describing the cavern area
    # store points as (y,x) with +y down so that reading order is natural sort order
    teams = {'E', 'G'}
    floors = {'E', 'G', '.'}
    f = input_string.split('\n')
    points = {(y, x): c for y, line in enumerate(f) for x, c in enumerate(line)}
    units = {point: Unit(c) for point, c in points.items() if c in teams}
    floor = {point for point, c in points.items() if c in floors}
    return units, floor


def adjacent_to(unit, units):
    adjacent = neighbors(unit)  # get adjacent squares
    enemies = {key for key, value in units.items() if value.team != units[unit].team}  # set of locations of other team
    targets = adjacent & enemies  # figure out which adjacent squares have enemies in them
    return targets, enemies


def get_paths(unit, floor_copy, in_range):
    queue = [(unit,)]
    paths = []
    minpath = len(floor_copy)
    while queue:  # BFS, queue items are a tuple of points representing a path
        current = queue.pop(0)
        if len(current) < minpath:  # don't explore paths that are longer than the current minimum
            # get neighbors of current tile, intersect with floor, and sort by reading order
            for new in sorted(neighbors(current[-1]) & floor_copy):
                new_path = current + (new,)
                if new in in_range:
                    paths.append(new_path)
                    floor_copy.discard(new)
                    minpath = min(minpath, len(new_path))
                else:
                    queue.append(new_path)
                    floor_copy.discard(new)
    return paths


def neighbors(point, cache={}):
    # return a set of the 4 points N, S, E, and W of point
    if point in cache:
        return cache[point]
    else:
        n = (point[0], point[1] - 1)
        s = (point[0], point[1] + 1)
        e = (point[0] - 1, point[1])
        w = (point[0] + 1, point[1])
        ret = {n, s, e, w}
        cache[point] = ret
        return ret


def attack(unit, units, attack_power):
    # attack according to the rules
    targets, enemies = adjacent_to(unit, units)  # set of adjacent enemies and locations of enemy team
    if targets:  # if there's anything left...
        # sort targets by hit points then by reading order
        targets = tuple(sorted(targets, key=lambda target: (units[target].hit_points, target)))
        target = targets[0]  # select the first target
        units[target].hit_points -= attack_power[units[unit].team]
        if units[target].hit_points <= 0:
            units.pop(target)


def move(unit, units, floor):
    # move unit according to the rules.  Return new unit location and whether or not there's any enemies around
    targets, enemies = adjacent_to(unit, units)  # set of adjacent enemies and all enemies
    if targets:  # unit is next to enemy, don't move
        return unit, True
    elif enemies:  # enemies exist, try to move to one
        in_range = set().union(*[neighbors(target) for target in enemies])  # all squares in-range of a target
        if unit in in_range:
            return unit, True
        else:
            in_range = in_range - units.keys()  # subtract other units
            in_range = in_range & floor  # can only travel within cavern
            floor_copy = floor.copy()  # area to explore
            floor_copy = floor_copy - units.keys()  # can't walk through units
            paths = get_paths(unit, floor_copy, in_range)
            if paths:  # if we found a path to a target...
                # sort paths by length and then by reading order of the endpoint
                # they should all be the same length but whatever...
                paths.sort(key=lambda x: (len(x), x[-1]))
                path = paths[0]  # pick first path
                new_unit = path[1]  # path[0] is where the unit is now, path[1] is first step along path
                units[new_unit] = units[unit]  # copy unit to new location
                units.pop(unit)  # delete unit at old location
                return new_unit, True
            else:  # unit did not move but there are enemies.  Combat continues.
                return unit, True
    else:  # no enemies, unit did not move.  Combat should end.
        return unit, False


def combat(units, floor, attack_power, verbose=False):
    rounds = 0
    while True:  # continue until return is called
        if verbose is True:
            visualize(units, floor, rounds)
        for unit in sorted(units.keys()):  # units take turns in reading order
            if unit in units:  # if the unit didn't just die...
                unit, targets_exist = move(unit, units, floor)
                if targets_exist:  # if there's any enemies left
                    attack(unit, units, attack_power)
                else:
                    # nobody to attack, end combat
                    if verbose is True:
                        visualize(units, floor, 'Finish!')
                    return rounds
        rounds += 1


def visualize(units, floor, rounds):
    # print round, current map of the board, and list of unit HP in reading order
    xn = min(floor, key=lambda x: x[1])[1]
    xx = max(floor, key=lambda x: x[1])[1]
    yn = min(floor)[0]
    yx = max(floor)[0]
    s = ''
    unitlist = []
    for y in range(yn, yx + 1):
        for x in range(xn, xx + 1):
            point = (y, x)
            if point in units:
                s += units[point].team
                unitlist.append(units[point].hit_points)
            elif point in floor:
                s += '.'
            else:
                s += '#'
        s += '\n'
    print('Round: ', rounds)
    print(s, end='')
    print('HP List: ', unitlist, end='\n\n')


def part1(input_string, attack_power=None, verbose=False):
    if attack_power is None:
        attack_power = {'G': 3, 'E': 3}
    units, floor = parse(input_string)
    elfcount = len({key for key, value in units.items() if value.team == 'E'})
    rounds = combat(units, floor, attack_power, verbose=False)
    outcome = rounds * sum([unit.hit_points for unit in units.values()])
    winner = list(units.values())[0].team
    teams = {'G': 'Goblin', 'E': 'Elf'}
    if verbose is True:
        print('Part 1')
        print('Outcome: ', outcome)
        print('Team ' + teams[winner] + ' wins.')
    elf_losses = elfcount - len({key for key, value in units.items() if value.team == 'E'})
    return elf_losses, outcome


def part2(input_string, verbose=False):
    attack_power = {'G': 3, 'E': 3}
    losses = 1
    while losses > 0:
        attack_power['E'] += 1
        losses, outcome = part1(input_string, attack_power, verbose=False)
    if verbose:
        print('Part 2')
        print('Elf attack power: ', attack_power['E'])
        print('No Elf losses!')
        print('Outcome: ', outcome)
    return outcome


def main(input_string, verbose=False):
    _, p1 = part1(input_string, verbose=verbose)
    p2 = part2(input_string, verbose=verbose)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2018, day=15, verbose=True)