import dancer
from common import graph, spatial as sp
from itertools import product


def least_losses(losses, minturn, maxturn):
    class Block:
        def __init__(self, loc, heading, count):
            self.loc = loc
            self.heading = heading
            self.count = count

        def neighbors(self):
            if self.count >= minturn:
                heading = self.heading.left()
                loc = self.loc + heading
                count = 1
                yield Block(loc, heading, count)
                heading = self.heading.right()
                loc = self.loc + heading
                count = 1
                yield Block(loc, heading, count)
            if self.count < maxturn:
                yield Block(self.loc + self.heading, self.heading, self.count+1)

        def __hash__(self):
            return hash((self.loc, self.heading, self.count))

        def __eq__(self, other):
            return self.loc == other.loc and self.heading == other.heading and self.count == other.count

        def __repr__(self):
            return f'{self.loc}; {self.heading}; {self.count}'

    def find_least_losses():
        pool, factory = sp.bounds(losses)
        city = graph.Graph()
        for loc, heading, count in product(losses.keys(), sp.ENWS, range(1, maxturn+1)):
            city.add_node(Block(loc, heading, count))
        for node in city.graph.keys():
            for neighbor in node.neighbors():
                if neighbor in city.graph:
                    city.add_edge_neq(node, neighbor, losses[neighbor.loc])
        targets = {Block(factory, heading, count) for heading in sp.ENWS for count in range(minturn, maxturn)}
        start = {Block(pool, heading, 1) for heading in sp.ENWS}
        return min(city.dijkstra(start, targets).values())

    return find_least_losses()


def main(input_string, verbose=False):
    losses = {a: int(b) for a, b in graph.text_to_dict(input_string).items()}
    p1 = least_losses(losses, minturn=1, maxturn=3)
    p2 = least_losses(losses, minturn=4, maxturn=10)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2023, day=17, verbose=True)
