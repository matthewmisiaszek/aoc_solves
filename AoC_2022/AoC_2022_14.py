import blitzen
from donner import spatial

ENTRANCE = spatial.Point(500, 0)
FALL_PRIORITY = (spatial.SOUTH, spatial.SOUTHWEST, spatial.SOUTHEAST)
FLOOR_HEIGHT = 2


def parse(input_string):
    rocks = set()
    for line in input_string.split('\n'):
        points = [spatial.Point(*[int(i) for i in point.split(',')]) for point in line.split(' -> ')]
        for a, b in zip(points, points[1:]):
            a, b = min(a, b), max(a, b)
            rocks.update({spatial.Point(x, y)
                          for y in range(a.y, b.y + 1)
                          for x in range(a.x, b.x + 1)})
    return rocks


def main(input_string, verbose=False):
    rocks = parse(input_string)
    floor = max(rock.y for rock in rocks) + FLOOR_HEIGHT
    turtle = spatial.Turtle(position=ENTRANCE)
    turtle.visited.update(rocks)
    p1 = None
    while True:
        for d in FALL_PRIORITY:
            position, new = turtle.move(d, peek=True)
            if new:
                if position.y < floor:
                    turtle.goto(position=position)
                    break
                elif p1 is None:
                    p1 = len(turtle.visited) - len(rocks) - len(turtle.history)
        else:
            if len(turtle.history) == 1:
                break
            turtle.revert()
    p2 = len(turtle.visited) - len(rocks)
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2022, day=14, verbose=True)
