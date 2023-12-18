import dancer
from common import graph, spatial as sp
from itertools import product


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
    minturn = Crucible.minturn
    maxturn = Crucible.maxturn
    pool, factory = sp.bounds(losses)
    city = graph.Graph()
    for loc, heading, count in product(losses.keys(), sp.ENWS, range(1, maxturn+1)):
        city.add_node(Crucible(loc, heading, count))
    for node in city.graph.keys():
        for neighbor in node.neighbors():
            if neighbor in city.graph:
                city.add_edge_neq(node, neighbor, losses[neighbor.loc])
    targets = {Crucible(factory, heading, count) for heading in sp.ENWS for count in range(minturn, maxturn)}
    start = {Crucible(pool, heading, 1) for heading in sp.ENWS}
    return min(city.dijkstra(start, targets).values())


def main(input_string, verbose=False):
    losses = {a: int(b) for a, b in graph.text_to_dict(input_string).items()}
    p1 = least_losses(losses)
    Crucible.minturn = 4
    Crucible.maxturn = 10
    p2 = least_losses(losses)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2023, day=17, verbose=True)
