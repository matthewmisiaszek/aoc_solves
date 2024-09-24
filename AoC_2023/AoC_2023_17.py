import blitzen
from donner import graph, spatial as sp, bfsqueue
from recordclass import dataobject
from typing import ClassVar


class Crucible(dataobject, readonly=True, hashable=True):
    minturn: ClassVar[int] = 1
    maxturn: ClassVar[int] = 3
    loc: sp.Point
    heading: sp.Point
    count: int = 0

    def neighbors(self):
        if self.count >= Crucible.minturn:
            for heading in (self.heading.right(), self.heading.left()):
                yield Crucible(self.loc + heading, heading, 1)
        if self.count < Crucible.maxturn:
            yield Crucible(self.loc + self.heading, self.heading, self.count + 1)


def least_losses(losses):
    pool, factory = sp.bounds(losses)
    start = {Crucible(pool, heading, 1): -losses[pool] for heading in sp.ENWS}
    q = bfsqueue.BFSQ(start)
    for curr, loss in q:
        if curr.loc not in losses:
            continue
        loss += losses[curr.loc]
        if curr.loc == factory:
            return loss
        for neighbor in curr.neighbors():
            q.add(neighbor, loss)


@blitzen.run
def main(input_string, verbose=False):
    losses = {a: int(b) for a, b in graph.text_to_dict(input_string).items()}
    p1 = least_losses(losses)
    Crucible.minturn = 4
    Crucible.maxturn = 10
    p2 = least_losses(losses)
    return p1, p2

