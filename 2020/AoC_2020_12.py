import sys
sys.path.append('..')
from common.aoc_input import aoc_input
from common.timer import timer
from common import constants as con
from common.elementwise import emulsum, eabsdiff


def part1(actions, loc, heading):
    circle = 360
    for action, value in actions:
        if action == con.Forward:
            loc = emulsum(loc, con.NSEW[heading], value)
        elif action == con.Left:
            heading = con.Headings[(con.Headings[heading] + value) % circle]
        elif action == con.Right:
            heading = con.Headings[(con.Headings[heading] - value) % circle]
        elif action in con.NSEW:
            loc = emulsum(loc, con.NSEW[action], value)
    return sum(eabsdiff(loc, con.origin2))


def part2(actions, ship, waypoint):
    ninety = 90
    for action, value in actions:
        if action == con.Forward:
            ship = emulsum(ship, waypoint, value)
        elif action == con.Left:
            for _ in range(value // ninety):
                x, y = waypoint
                waypoint = -y, x
        elif action == con.Right:
            for _ in range(value // ninety):
                x, y = waypoint
                waypoint = y, -x
        elif action in con.NSEW:
            waypoint = emulsum(waypoint, con.NSEW[action], value)
    return sum(eabsdiff(ship, con.origin2))


def main(input_string, verbose=False):
    actions = tuple((action[0], int(action[1:])) for action in input_string.split('\n'))
    p1 = part1(actions, con.origin2, con.East)
    p2 = part2(actions, con.origin2, (10, 1))
    if verbose:
        print('Part 1: {0[0]}\nPart 2: {0[1]}'.format([p1, p2]))
    return p1, p2


if __name__ == "__main__":
    main(aoc_input(2020, 12), verbose=True)
    print('Time:  ', timer())
