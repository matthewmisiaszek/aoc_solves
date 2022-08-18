from queue import PriorityQueue


def merge_two_dicts(x, y):
    z = x.copy()  # start with keys and values of x
    z.update(y)  # modifies z with keys and values of y
    return z


def shortest_path(start, end, cave):
    q = PriorityQueue()
    q.put((0, start))
    while not q.empty():
        dist, loc = q.get()
        for n in neighbors(cave, loc):
            if n == end:
                return dist + cave[n]
            q.put((dist + cave[n], n))
            cave.pop(n)


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
    return minbound, maxbound


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
    cave2 = cave.copy()
    p1 = shortest_path((0, 0), ubound, cave)
    expand(cave2)
    ubound = bounds(cave2)[1]
    p2 = shortest_path((0, 0), ubound, cave2)

    if verbose:
        print('Part 1: {0[0]}\nPart 2: {0[1]}'.format([p1, p2]))
    return p1, p2


if __name__ == "__main__":
    main(verbose=True)
