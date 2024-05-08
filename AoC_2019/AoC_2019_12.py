import blitzen
import re
import math


def manhattan(a):
    return sum((abs(i) for i in a))


def sum_tuple(a, b):
    return tuple(ai + bi for ai, bi in zip(a, b))


def gravity(pos, vel, moon_positions):
    vel = list(vel)
    for moon in moon_positions:
        for axis in range(3):
            if moon[axis] > pos[axis]:
                vel[axis] += 1
            elif moon[axis] < pos[axis]:
                vel[axis] -= 1
    return tuple(vel)


@blitzen.run
def main(input_string, verbose=False):
    pattern = '<x=(.*), y=(.*), z=(.*)>'
    moon_positions = tuple(tuple(int(i) for i in moon)
                           for moon in re.findall(pattern, input_string))
    moon_velocities = tuple((0,) * 3 for _ in moon_positions)
    initial_positions = moon_positions
    initial_velocities = moon_velocities
    periods = {}
    steps = 0
    while steps < 1000 or len(periods) < 3:
        moon_velocities = tuple(gravity(pos, vel, moon_positions)
                                for pos, vel in zip(moon_positions, moon_velocities))
        moon_positions = tuple(sum_tuple(pos, vel)
                               for pos, vel in zip(moon_positions, moon_velocities))
        steps += 1

        if steps == 1000:
            p1 = sum(manhattan(mpos) * manhattan(mvel)
                     for mpos, mvel in zip(moon_positions, moon_velocities))

        for axis, (p, v, ip, iv) in enumerate(zip(
                zip(*moon_positions), zip(*moon_velocities),
                zip(*initial_positions), zip(*initial_velocities))):
            if axis not in periods and (v == iv) and (p == ip):
                periods[axis] = steps

    p2 = math.lcm(*periods.values())
    return p1, p2

