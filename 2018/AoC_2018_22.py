import core
from queue import PriorityQueue


class Cave:
    def __init__(self, input_string):
        f = input_string.split('\n')
        self.depth = int(f[0].split()[1])
        self.target = (int(f[1].split()[1].split(',')[0]), int(f[1].split()[1].split(',')[1]))
        self.types = {}
        self.erosion_level = {}
        self.base = 20183
        self.types_tools = set()
        self.chunk = 10

    def get_type(self, point):
        tools = [{'climbing gear', 'torch'}, {'climbing gear', 'neither'}, {'torch', 'neither'}]
        if point in self.types:
            return self.types[point]
        else:
            to_check = {(x, y) for x in range(0, point[0] + 1) for y in range(0, point[1] + 1)}
            to_check = to_check - self.types.keys()
            for checkpoint in sorted(to_check):
                if checkpoint == (0, 0) or checkpoint == self.target:
                    erosion_level = +self.depth % self.base
                elif checkpoint[0] == 0:
                    erosion_level = (checkpoint[1] * 48271 + self.depth) % self.base
                elif checkpoint[1] == 0:
                    erosion_level = (checkpoint[0] * 16807 + self.depth) % self.base
                else:
                    a = (checkpoint[0] - 1, checkpoint[1])
                    b = (checkpoint[0], checkpoint[1] - 1)
                    erosion_level = (self.erosion_level[a] * self.erosion_level[b] + self.depth) % self.base
                self.erosion_level[checkpoint] = erosion_level
                type = erosion_level % 3
                self.types[checkpoint] = type
                for tool in tools[type]:
                    self.types_tools.add((checkpoint, tool))
            return type

    def get_neighbors(self, key):
        ret = {}
        loc, tool = key
        n = (loc[0], loc[1] - 1)
        s = (loc[0], loc[1] + 1)
        e = (loc[0] + 1, loc[1])
        w = (loc[0] - 1, loc[1])
        for neighbor in (n, s, e, w):
            ret[(neighbor, tool)] = 1
        for tool in {'climbing gear', 'torch', 'neither'} - {tool}:
            ret[(loc, tool)] = 7
        return ret

    def print_types(self):
        xn, xx, yn, yx = self.getbounds()
        s = ''
        types = ['.', '=', '|']
        for y in range(yn, yx + 1):
            for x in range(xn, xx + 1):
                point = (x, y)
                if point in self.types:
                    s += types[self.types[point]]
                else:
                    s += ' '
            s += '\n'
        print(s)

    def getbounds(self):
        yn = min(self.types.keys(), key=lambda x: x[1])[1]
        yx = max(self.types.keys(), key=lambda x: x[1])[1]
        xn = min(self.types.keys())[0]
        xx = max(self.types.keys())[0]
        return xn, xx, yn, yx

    def test_node(self, node):

        loc, tool = node
        x, y = loc
        if x >= 0 and y >= 0:
            if loc not in self.types:
                xn, xx, yn, yx = self.getbounds()
                if x > xx:
                    xx = max(x, xx + self.chunk)
                if y > yn:
                    yx = max(y, yx + self.chunk)
                self.get_type((xx, yx))
            return node in self.types_tools
        else:
            return False

    def heur(self, point):
        return abs(point[0] - self.target[0]) + abs(point[1] - self.target[1])


def main(input_string, verbose=False):
    cave = Cave(input_string)
    cave.get_type(cave.target)
    if verbose:
        cave.print_types()
    p1 = sum(cave.types.values())
    queue = PriorityQueue()
    queue.put((0, 0, (0, 0), 'torch'))
    closed = set()
    while not queue.empty():
        heur, time, loc, tool = queue.get()
        if (loc, tool) == (cave.target, 'torch'):
            break
        elif (loc, tool) not in closed:
            closed.add((loc, tool))
            neighbors = cave.get_neighbors((loc, tool))
            for node in (neighbors.keys() - closed) & cave.types_tools:
                nloc, ntool = node
                queue.put((cave.heur(nloc) + time + neighbors[node], time + neighbors[node], nloc, ntool))
            for node in neighbors.keys() - closed - cave.types_tools:
                if cave.test_node(node):
                    nloc, ntool = node
                    queue.put((cave.heur(nloc) + time + neighbors[node], time + neighbors[node], nloc, ntool))
                else:
                    closed.add(node)
    p2 = time
    return p1, p2


if __name__ == "__main__":
    core.run(main, year=2018, day=22, verbose=True)
