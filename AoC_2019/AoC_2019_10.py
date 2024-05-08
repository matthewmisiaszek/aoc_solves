import blitzen
import math
from itertools import product
from collections import defaultdict
from donner import graph


def get_sight_lines(asteroids):
    all_sight_lines = {asteroid: defaultdict(list) for asteroid in asteroids}
    for a, b in product(asteroids, asteroids):
        if a != b:
            d = b - a
            aa = -math.atan2(d.x, d.y)
            all_sight_lines[a][aa].append(b)
    return all_sight_lines


def giant_laser(station_sight_lines, station):
    for line in station_sight_lines.values():
        line.sort(key=lambda x: x.manhattan(station))
    sorted_sight_lines = [station_sight_lines[angle] for angle in sorted(station_sight_lines.keys())]
    vaporized = []
    while sorted_sight_lines:
        vaporized += [line.pop(0) for line in sorted_sight_lines]
        sorted_sight_lines = [line for line in sorted_sight_lines if line]
    return vaporized


@blitzen.run
def main(input_string, verbose=False):
    asteroids = graph.text_to_dict(input_string, exclude='.')
    all_sight_lines = get_sight_lines(asteroids)

    station = max(all_sight_lines.keys(), key=lambda angle: len(all_sight_lines[angle]))
    station_sight_lines = all_sight_lines[station]
    p1 = len(station_sight_lines)

    vaporized = giant_laser(station_sight_lines, station)
    v = vaporized[199]
    p2 = 100 * v.x + v.y
    return p1, p2

