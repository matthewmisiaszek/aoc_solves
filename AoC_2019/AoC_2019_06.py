import blitzen


def main(input_string, verbose=False):
    com, you, san = 'COM', 'YOU', 'SAN'
    q = [com]
    paths = {com: set()}
    orbits = [tuple(line.split(')')) for line in input_string.split('\n')]
    orbits = {a: {b[1] for b in orbits if b[0] == a} for a in sum(orbits, ())}
    while q:
        paths.update({b: paths[q[0]].union({q[0]}) for b in orbits[q[0]]})
        q = q[1:] + list(orbits[q[0]])
    p1 = sum([len(i) for i in paths.values()])
    p2 = len(paths[you].symmetric_difference(paths[san]))
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2019, day=6, verbose=True)
