from queue import PriorityQueue


def merge_two_dicts(x, y):
    z = x.copy()  # start with keys and values of x
    z.update(y)  # modifies z with keys and values of y
    return z


def dijkstras(start, end, cave):
    q, closed = PriorityQueue(), [{}, {}]
    q.put((0, start, 0))  # start from start
    q.put((cave[end], end, 1))  # start from end
    solves = []  # list of potential paths
    mate = False  # have any paths been found yet?
    while not q.empty():  # run the queue dry
        dist, loc, side = q.get()
        if loc in closed[1 - side]:  # if this location was visited from other side, this is a path
            mate = True  # path found, stop adding to queue
            solves.append(dist + closed[1 - side][loc] - cave[loc])  # add to list of potential paths
        elif not mate:  # if not a path and no paths yet, add to queue
            if loc not in closed[side]:  # don't check places you've already been
                closed[side][loc] = dist  # record risk it takes to get to this point from this side
                for n in neighbors(cave, loc):
                    if n not in closed[side]:  # don't add places you've already been
                        q.put((dist + cave[n], n, side))
    # common.printgrid(merge_two_dicts(closed[0], closed[1]))
    return min(solves)  # return the shortest of all found paths


def makegrid(f):
    grid = {}
    for y, line in enumerate(f):
        for x, c in enumerate(line):
            grid[(x, y)] = int(c)
    return grid


def neighbors(grid, point):
    ret = []
    for offset in ((0, 1), (1, 0), (0, -1), (-1, 0)):
        new_point = (point[0] + offset[0], point[1] + offset[1])
        if new_point in grid:
            ret.append(new_point)
    return ret


def bounds(grid):
    minbound = tuple([min(grid.keys(), key=lambda x: x[i])[i] for i in (0, 1)])
    maxbound = tuple([max(grid.keys(), key=lambda x: x[i])[i] for i in (0, 1)])
    return (minbound, maxbound)


def expand(cave):
    repeat = 5
    ubound = bounds(cave)[1]
    for key in tuple(cave.keys()):
        val = cave[key]
        for x in range(repeat):
            for y in range(repeat):
                ngrid = (x, y)
                if not ngrid == (0, 0):
                    nkey = tuple(key[i] + (ubound[i] + 1) * ngrid[i] for i in range(2))
                    nval = (val + x + y - 1) % 9 + 1
                    cave[nkey] = nval


def main(input_file='input.txt', verbose=False):
    f = open(input_file).read().split('\n')
    cave = makegrid(f)
    ubound = bounds(cave)[1]
    p1 = dijkstras((0, 0), ubound, cave)
    expand(cave)
    ubound = bounds(cave)[1]
    p2 = dijkstras((0, 0), ubound, cave)

    if verbose:
        print('Part 1: {0[0]}\nPart 2: {0[1]}'.format([p1, p2]))
    return p1, p2


if __name__ == "__main__":
    main(verbose=True)
