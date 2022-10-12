import dancer
from common.misc import digits
from common import elementwise as ew, constants as con


def is_space(point, fav):
    x, y = point
    if x >= 0 and y >= 0:
        val = x * x + 3 * x + 2 * x * y + y + y * y + fav
        return sum(digits(val, 2)) % 2 == 0
    else:
        return False


def main(input_string, verbose=False):
    loc, target = (1, 1), (31, 39)
    max_steps = 50
    closed = set()
    fav = int(input_string)
    p1, p2 = None, set()
    queue = [(0, loc)]
    while p1 is None or steps <= max_steps:
        steps, loc = queue.pop(0)
        if p1 is None and loc == target:
            p1 = steps
        if steps <= max_steps:
            p2.add(loc)
        for direction in con.D2D4:
            neighbor = ew.sum2d(loc, direction)
            if neighbor not in closed:
                closed.add(neighbor)
                if is_space(neighbor, fav):
                    queue.append((steps + 1, neighbor))
    p2 = len(p2)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2016, day=13, verbose=True)
