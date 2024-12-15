import blitzen
from donner import spatial, printer


class Box:
    def __init__(self, position, size, btype, grid):
        self.p = position
        self.s = size
        self.shape = {spatial.Point(x, y) for x in range(size.x) for y in range(size.y)}
        self.type = btype
        self.grid = grid
        for s in self.shape:
            self.grid[self.p + s] = self

    def move(self, d, check=True):
        if self.type == '#':
            return False
        np = self.p + d
        for s in self.shape:
            q = s + np
            if q in self.grid:
                if self.grid[s + np] == self:
                    continue
                if self.grid[s + np].move(d, check) is False:
                    return False
        if check:
            return True
        for s in self.shape:
            self.grid.pop(self.p + s)
        self.p = np
        for s in self.shape:
            self.grid[self.p + s] = self
        return True


def warehouse_sim(input_string, scale, verbose):
    warehouse, moves = input_string.split("\n\n")
    grid = {}
    boxes = []
    for y, line in enumerate(warehouse.split('\n')):
        for x, c in enumerate(line):
            if c == '.':
                continue
            size = spatial.Point(1, 1) if c == '@' else scale
            box = Box(spatial.Point(x, y) * scale, size, c, grid)
            if c == 'O':
                boxes.append(box)
            if c == '@':
                fish = box
    for move in moves.strip():
        if move == '\n':
            continue
        move = spatial.NAMES_2D[move]
        if fish.move(move):
            fish.move(move, check=False)
    if verbose:
        printer.printdict({p: v.type for p, v in grid.items()})
    return sum((b.p.x * 1 + b.p.y * 100 for b in boxes))


@blitzen.run
def main(input_string, verbose=False):
    p1 = warehouse_sim(input_string, spatial.Point(1, 1), verbose)
    p2 = warehouse_sim(input_string, spatial.Point(2, 1), verbose)
    return p1, p2
