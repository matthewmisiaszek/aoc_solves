import dancer
from common import spatial

ROCK = '#'
JET_DIRECTIONS = {'>': spatial.EAST,
                  '<': spatial.WEST}
DOWN = spatial.SOUTH
LBOUND = 0
RBOUND = 6


def get_rocks():
    rock_file = open(dancer.root_path + '/AoC_2022/rocks').read().strip()
    rocks = []
    for rock in rock_file.split('\n\n'):
        rock = tuple(spatial.Point(x, y).yinv()
                     for y, line in enumerate(reversed(rock.split('\n')))
                     for x, c in enumerate(line)
                     if c is ROCK)
        rocks.append(rock)
    return tuple(rocks)


def move(rock_location, rock_shape, direction, settled):
    rock_location += direction
    for point in rock_shape:
        point += rock_location
        if point in settled:
            break
        if not (LBOUND <= point.x <= RBOUND):
            break
    else:
        return rock_location, True
    rock_location -= direction
    return rock_location, False


def main(input_string, verbose=False):
    jets = tuple(JET_DIRECTIONS[i] for i in input_string)
    rocks = get_rocks()
    rock_index = jet_index = top = bottom = rock_number = 0
    history_list = []  # time history of where the top of the stack is
    history_dict = {}  # used for checking for repeat.  value is when the key occurred and the top at that time
    settle_history = [0] * len(rocks)  # x location of the last five rocks to fall, used to make key
    settled = {spatial.Point(x, 0) for x in
               range(LBOUND, RBOUND + 1)}  # rocks that have settled.  Initialize with floor.
    while True:
        rock_shape = rocks[rock_index]
        rock_index += 1
        rock_index %= len(rocks)
        rock_location = spatial.Point(LBOUND + 2, top - 4)  # 2 units from left wall, 3 units from top
        while True:
            rock_location, _ = move(rock_location, rock_shape, jets[jet_index], settled)  # apply jet
            jet_index += 1
            jet_index %= len(jets)
            rock_location, drop = move(rock_location, rock_shape, DOWN, settled)  # try to drop
            if drop is False:
                break  # rock is settled
        settle_history.append(rock_location.x)
        settle_history.pop(0)
        settled.update({rock_location + point for point in rock_shape})  # add rock to settled
        peaks = [min(point.y for point in settled if point.x == x) for x in range(LBOUND, RBOUND + 1)]
        top = min(peaks)
        key = (tuple(settle_history), rock_index, jet_index)
        if key in history_dict:
            break  # it repeated. We can extrapolate from here!
        else:
            history_dict[key] = (top, rock_number)
            history_list.append(top)
            rock_number += 1
    # extrapolate!
    top0, rn0 = history_dict[key]
    rdelta = rock_number - rn0
    tdelta = top - top0
    for n in (2022, 1000000000000):
        n -= 1
        n -= rn0
        repeat = n // rdelta
        extra = n % rdelta
        yield -1 * (tdelta * repeat + history_list[rn0 + extra])


if __name__ == "__main__":
    dancer.run(main, year=2022, day=17, verbose=True)
