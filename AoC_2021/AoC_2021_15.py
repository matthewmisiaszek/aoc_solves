import blitzen
from queue import PriorityQueue


def shortest_path(start, end, cave):
    q = PriorityQueue()
    q.put((0, start))
    while not q.empty():
        dist, loc = q.get()
        for offset in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            n = (loc[0] + offset[0], loc[1] + offset[1])
            if n in cave:
                if n == end:
                    return dist + cave[n]
                q.put((dist + cave[n], n))
                cave.pop(n)


def expand(cave, repeat=5):
    ux, uy = max(cave.keys())
    ux, uy = ux + 1, uy + 1
    for (kx, ky), val in tuple(cave.items()):
        for x in range(repeat):
            for y in range(repeat):
                if x or y:
                    nkey = (kx + ux * x, ky + uy * y)
                    nval = (val + x + y - 1) % 9 + 1
                    cave[nkey] = nval


def main(input_string, verbose=False):
    f = input_string.split('\n')
    cave = {}
    for y, line in enumerate(f):
        for x, c in enumerate(line):
            cave[(x, y)] = int(c)
    cave2 = cave.copy()
    p1 = shortest_path((0, 0), max(cave.keys()), cave)
    expand(cave2)
    p2 = shortest_path((0, 0), max(cave2.keys()), cave2)

    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2021, day=15, verbose=True)
