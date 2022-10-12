import dancer
from common.misc import md5hash
from common import elementwise as ew, constants as con


def main(input_string, verbose=False):
    loc = con.origin2
    target = (3, 3)
    xn, xx = 0, 3
    yn, yx = 0, 3
    open_doors = {'b', 'c', 'd', 'e', 'f'}
    password = input_string
    queue = {('', loc)}
    paths = set()
    while queue:
        path, loc = queue.pop()
        x, y = loc
        if loc == target:
            paths.add(path)
        elif xn <= x <= xx and yn <= y <= yx:
            path_hash = md5hash(password + path)
            for direction, door in zip(con.UDLR_ordered, path_hash):
                if door in open_doors:
                    nloc = ew.sum2d(loc, con.UDLR_YINV[direction])
                    npath = path + direction
                    queue.add((npath, nloc))
    p1 = min(paths, key=lambda n: len(n))
    p2 = len(max(paths, key=lambda n: len(n)))
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2016, day=17, verbose=True)
