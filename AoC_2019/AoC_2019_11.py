import blitzen
from AoC_2019.intcode import Intcode
from donner import printer, spatial


def emergency_hull_painting_robot(brain, starting_panel):
    brain.load_state()
    hull, painted = set(), set()
    loc, heading = spatial.Point(), spatial.NORTH
    if starting_panel is True:
        hull.add(loc)

    while brain.status != 0:
        is_painted = int(loc in hull)
        while len(brain.output) < 2:
            brain.run(is_painted)

        paint = brain.output.pop(0)
        if paint == 1:
            hull.add(loc)
        else:
            hull.discard(loc)
        painted.add(loc)

        turn = brain.output.pop(0)
        if turn == 1:
            heading = heading.right()
        else:
            heading = heading.left()
        loc+= heading
    return len(painted), printer.strset(hull)


@blitzen.run
def main(input_string, verbose=False):
    program = [int(i) for i in input_string.split(',')]
    brain = Intcode(program)
    p1, _ = emergency_hull_painting_robot(brain, False)
    _, p2 = emergency_hull_painting_robot(brain, True)
    p2 = printer.ocr(p2)
    return p1, p2

