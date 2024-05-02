import blitzen
from donner import graph, spatial


ROUND = 'O'
SPACE = '.'
ONE_BILLION = 1000000000


def tilt(platform, direction):
    round_rocks = set(rock for rock, ch in platform.items() if ch == ROUND)
    bounds = spatial.bounds(platform)
    load = 0
    for rock in sorted(round_rocks, key=lambda x: x*direction, reverse=True):
        platform.pop(rock)
        while spatial.inbounds(rock, bounds) and rock not in platform:
            rock += direction
        rock -= direction
        platform[rock] = ROUND
        load += bounds[1].y - rock.y + 1
    return load


def main(input_string, verbose=False):
    p1 = p2 = None
    platform = graph.text_to_dict(input_string, exclude=SPACE)
    history, repeat = [], {}
    for cycle in range(ONE_BILLION):
        for direction in (spatial.NORTH, spatial.WEST, spatial.SOUTH, spatial.EAST):
            load = tilt(platform, direction)
            if p1 is None:
                p1 = load
        hkey = tuple(sorted((key for key, val in platform.items() if val == ROUND)))
        history.append(load)
        if hkey in repeat:
            b = repeat[hkey]
            m = cycle - b
            p2 = history[(ONE_BILLION - repeat[hkey] - 1) % m + b]
            break
        repeat[hkey] = cycle
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2023, day=14, verbose=True)
