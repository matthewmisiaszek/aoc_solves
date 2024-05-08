import blitzen
from donner import spatial as sp


def part1(actions, loc, heading):
    for action, value in actions:
        if action == 'F':
            loc += heading*value
        elif action == 'L':
            for _ in range(value // 90):
                heading = heading.left()
        elif action == 'R':
            for _ in range(value // 90):
                heading = heading.right()
        elif action in sp.NAMES_2D:
            loc += sp.NAMES_2D[action] * value
    return loc.manhattan()


def part2(actions, ship, waypoint):
    ninety = 90
    for action, value in actions:
        if action == 'F':
            ship += waypoint * value
        elif action == 'L':
            for _ in range(value // ninety):
                waypoint = waypoint.left()
        elif action == 'R':
            for _ in range(value // ninety):
                waypoint = waypoint.right()
        elif action in sp.NAMES_2D:
            waypoint += sp.NAMES_2D[action] * value
    return ship.manhattan()


@blitzen.run
def main(input_string, verbose=False):
    actions = tuple((action[0], int(action[1:])) for action in input_string.split('\n'))
    p1 = part1(actions, sp.Point(), sp.EAST)
    p2 = part2(actions, sp.Point(), sp.EAST * 10 + sp.NORTH * 1)
    return p1, p2

