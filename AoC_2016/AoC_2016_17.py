import blitzen
from donner.misc import md5hash
from donner import spatial as sp


UDLR = (sp.NORTH, sp.SOUTH, sp.WEST, sp.EAST)


@blitzen.run
def main(input_string, verbose=False):
    loc = sp.Point()
    target = sp.Point(3, 3)
    bounds = sp.Point(), sp.Point(3, 3)
    open_doors = {'b', 'c', 'd', 'e', 'f'}
    password = input_string
    queue = {('', loc)}
    paths = set()
    while queue:
        path, loc = queue.pop()
        if loc == target:
            paths.add(path)
        elif sp.inbounds(loc, bounds):
            path_hash = md5hash(password + path)
            for dname, direction, door in zip('UDLR', UDLR, path_hash):
                if door in open_doors:
                    nloc = loc + direction
                    npath = path + dname
                    queue.add((npath, nloc))
    p1 = min(paths, key=lambda n: len(n))
    p2 = len(max(paths, key=lambda n: len(n)))
    return p1, p2

