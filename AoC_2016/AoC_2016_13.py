import dancer
from common.misc import digits
from common import elementwise as ew, constants as con, bfsqueue


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
    fav = int(input_string)
    p1, p2 = None, set()
    queue = bfsqueue.BFSQ(loc)
    for loc, steps in queue:
        if p1 is None and loc == target:
            p1 = steps
        if steps <= max_steps:
            p2.add(loc)
        if p1 is None or steps < max_steps:
            for direction in con.D2D4:
                neighbor = ew.sum2d(loc, direction)
                if is_space(neighbor, fav):
                    queue.add(neighbor, steps+1)
    p2 = len(p2)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2016, day=13, verbose=True)
