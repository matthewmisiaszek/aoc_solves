import blitzen
from donner import spatial, printer
import re
from collections import Counter
from math import prod


class Bot:
    def __init__(self, p, v, bounds):
        self.p = spatial.Point(int(p[0]), int(p[1]))
        self.v = spatial.Point(int(v[0]), int(v[1]))
        self.bounds = bounds

    def move(self):
        self.p = (self.p + self.v) % self.bounds

    def quadrant(self):
        m = self.bounds // 2
        if self.p.x == m.x or self.p.y == m.y:
            return 0
        x = self.p.x < m.x
        y = self.p.y < m.y
        return (x,y)


def solve(bots, bounds):
    seconds = 0
    while True:
        seconds += 1
        for bot in bots:
            bot.move()
        if seconds == 100:
            quadrants = Counter([bot.quadrant() for bot in bots])
            if 0 in quadrants:
                quadrants.pop(0)
            p1 = prod(quadrants.values())
        botset = {bot.p for bot in bots}
        for x in range(bounds.x):
            line = 0
            for y in range(0, bounds.y):
                if spatial.Point(x, y) in botset:
                    line += 1
                else:
                    line = 0
                if line > 10:
                    return p1, seconds


@blitzen.run
def main(input_string, verbose=False):
    bounds = spatial.Point(101,103,1)
    bots = [
        Bot((px, py), (vx, vy), bounds)
        for px, py, vx, vy in re.findall(r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)', input_string)
    ]
    p1, p2 = solve(bots, bounds)
    if verbose:
        printer.printset({bot.p for bot in bots})
    return p1, p2

