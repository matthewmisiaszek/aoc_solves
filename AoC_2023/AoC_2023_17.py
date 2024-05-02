import blitzen
from donner import graph, spatial as sp, bfsqueue


class Crucible:
    minturn = 1
    maxturn = 3

    def __init__(self, loc, heading, count):
        self.loc = loc
        self.heading = heading
        self.count = count

    def neighbors(self):
        if self.count >= Crucible.minturn:
            heading = self.heading.left()
            loc = self.loc + heading
            count = 1
            yield Crucible(loc, heading, count)
            heading = self.heading.right()
            loc = self.loc + heading
            count = 1
            yield Crucible(loc, heading, count)
        if self.count < Crucible.maxturn:
            yield Crucible(self.loc + self.heading, self.heading, self.count + 1)

    def __hash__(self):
        return hash((self.loc, self.heading, self.count))

    def __eq__(self, other):
        return self.loc == other.loc and self.heading == other.heading and self.count == other.count

    def __repr__(self):
        return f'{self.loc}; {self.heading}; {self.count}'


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


def main(input_string, verbose=False):
    losses = {a: int(b) for a, b in graph.text_to_dict(input_string).items()}
    p1 = least_losses(losses)
    Crucible.minturn = 4
    Crucible.maxturn = 10
    p2 = least_losses(losses)
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2023, day=17, verbose=True)
