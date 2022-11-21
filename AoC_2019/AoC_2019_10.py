import dancer
import math
from common.elementwise import manhattan
from itertools import product
from collections import defaultdict


def parse(input_string):
    asteroid = '#'
    asteroids = {(x, y)
                 for y, line in enumerate(input_string.split('\n'))
                 for x, c in enumerate(line)
                 if c is asteroid}
    return asteroids


def get_sight_lines(asteroids):
    all_sight_lines = {asteroid: defaultdict(list) for asteroid in asteroids}
    for a, b in product(asteroids, asteroids):
        if a != b:
            ax, ay = a
            bx, by = b
            dx = (bx - ax)
            dy = (by - ay)
            aa = -math.atan2(dx, dy)
            all_sight_lines[a][aa].append(b)
    return all_sight_lines


def giant_laser(station_sight_lines, station):
    for line in station_sight_lines.values():
        line.sort(key=lambda x: manhattan(x, station))
    sorted_sight_lines = [station_sight_lines[angle] for angle in sorted(station_sight_lines.keys())]
    keysort = sorted(station_sight_lines.keys())
    vaporized = []
    while sorted_sight_lines:
        vaporized += [line.pop(0) for line in sorted_sight_lines]
        sorted_sight_lines = [line for line in sorted_sight_lines if line]
    return vaporized


def main(input_string, verbose=False):
    asteroids = parse(input_string)
    all_sight_lines = get_sight_lines(asteroids)

    station = max(all_sight_lines.keys(), key=lambda angle: len(all_sight_lines[angle]))
    station_sight_lines = all_sight_lines[station]
    p1 = len(station_sight_lines)

    vaporized = giant_laser(station_sight_lines, station)
    x, y = vaporized[199]
    p2 = 100 * x + y
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2019, day=10, verbose=True)
