import blitzen
from donner import graph, spatial


def main(input_string, verbose=False):
    p1 = p2 = 0
    for pattern in input_string.split('\n\n'):
        pattern = graph.text_to_dict(pattern, include='#')
        bn, bx = spatial.bounds(pattern.keys())
        for axis, fact in (('x', 1), ('y', 100)):
            for mirror in range(bn.asdict()[axis] + 1, bx.asdict()[axis] + 1):
                smudge = 0
                for rock in pattern:
                    reflected = rock.asdict()
                    reflected[axis] = mirror - (reflected[axis] - mirror + 1)
                    reflected = spatial.Point(**reflected)
                    if spatial.inbounds(reflected, (bn, bx)) and reflected not in pattern:
                        smudge += 1
                if smudge == 0:
                    p1 += mirror * fact
                if smudge == 1:
                    p2 += mirror * fact
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2023, day=13, verbose=True)
