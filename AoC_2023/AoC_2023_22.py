import dancer
from common import spatial
from itertools import product
from collections import defaultdict


class Block:
    def __init__(self, line, stack):
        self.line = line
        self.corners = tuple(spatial.Point3D(
            *(int(i) for i in point.split(','))
            ) for point in line.split('~'))
        self.nb, self.xb = spatial.bounds3D(self.corners)
        self.footprint = {
            spatial.Point(x, y): self 
            for x, y in product(
                    range(self.nb.x, self.xb.x+1), 
                    range(self.nb.y, self.xb.y+1)
                    )
            }
        self.z = self.nb.z
        self.height = self.xb.z - self.nb.z + 1
        self.stack = stack
        self.on = set()
        self.under = set()
    
    def fall(self):
        footset = set(self.footprint)
        z = max(self.stack) if self.stack else 1
        while z > 1 and not set(self.stack[z]) & footset:
            z -= 1
        for point in set(self.stack[z]) & footset:
            other = self.stack[z][point]
            other.under.add(self)
            self.on.add(other)
        self.z = z + 1
        for z in range(self.z, self.z + self.height):
            self.stack[z].update(self.footprint)
    
    def n_fall(self, chain=None):
        if chain is None:
            chain = set()
        chain.add(self)
        for other in self.under:
            if not other.on - chain:
                other.n_fall(chain)
        return len(chain)
    
    def __lt__(self, other):
        return self.z < other.z
    
    def __hash__(self):
        return hash(self.line)
    
    def __eq__(self, other):
        return self.line == other.line


def main(input_string, verbose=False):
    stack = defaultdict(dict)
    blocks = [Block(line, stack) for line in input_string.split('\n')]
    blocks.sort()
    for block in blocks:
        block.fall()
    p1 = sum(block.n_fall() == 1 for block in blocks)
    
    p2 = sum(block.n_fall() for block in blocks) - len(blocks)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2023, day=22, verbose=True)
