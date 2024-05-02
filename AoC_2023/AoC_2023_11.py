import blitzen
from donner import graph, spatial
from itertools import combinations


def main(input_string, verbose=False):
    galaxies = graph.text_to_dict(input_string, include='#')
    bn, bx = spatial.bounds(galaxies)
    xno = set(range(bn.x, bx.x + 1)) - set(g.x for g in galaxies)
    yno = set(range(bn.y, bx.y + 1)) - set(g.y for g in galaxies)
    for expansion in 1, 999999:
        expanded_galaxies = {
            spatial.Point(
                g.x + sum(i < g.x for i in xno) * expansion,
                g.y + sum(i < g.y for i in yno) * expansion
            )
            for g in galaxies
        }
        yield sum(a.manhattan(b) for a, b in combinations(expanded_galaxies, 2))


if __name__ == "__main__":
    blitzen.run(main, year=2023, day=11, verbose=True)
