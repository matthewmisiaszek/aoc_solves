import dancer
from common import printer

INTERESTING = {20, 60, 100, 140, 180, 220}
SCREEN_HEIGHT = 6
SCREEN_WIDTH = 40
NOOP = 'noop'


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
    pixels = [(col, row) for row in range(SCREEN_WIDTH) for col in range(SCREEN_WIDTH)]
    screen = {(col, row) for (col, row), x in zip(pixels, xregs) if abs(col - x) <= 1}
    p2 = printer.strset(screen)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2022, day=10, verbose=True)
