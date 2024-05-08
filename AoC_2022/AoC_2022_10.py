import blitzen
from donner import printer, spatial

INTERESTING = {20, 60, 100, 140, 180, 220}
SCREEN_HEIGHT = 6
SCREEN_WIDTH = 40
NOOP = 'noop'


@blitzen.run
def main(input_string, verbose=False):
    signal = input_string.split('\n')
    x = 1
    xregs = []
    for instruction in signal:
        xregs.append(x)
        if instruction != NOOP:
            xregs.append(x)
            _, inc = instruction.split()
            x += int(inc)
    p1 = sum(cycle * xregs[cycle-1] for cycle in INTERESTING)
    pixels = [spatial.Point(col, row) for row in range(SCREEN_WIDTH) for col in range(SCREEN_WIDTH)]
    screen = {point for point, x in zip(pixels, xregs) if abs(point.x - x) <= 1}
    p2 = printer.strset(screen)
    return p1, p2

