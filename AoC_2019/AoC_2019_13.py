import blitzen
from AoC_2019.intcode import Intcode
from donner import printer
from collections import Counter


SPACE, WALL, BLOCK, PADDLE, BALL = ' ', '|', '#', 'T', 'o'
SPRITES = (SPACE, WALL, BLOCK, PADDLE, BALL)


def sprites(idx):
    if idx >= len(SPRITES):
        return idx
    else:
        return SPRITES[idx]


def render(output, display, verbose):
    x, y, t = (output[i::3] for i in range(3))
    output.clear()
    display.update({(xi, yi): sprites(ti) for xi, yi, ti in zip(x, y, t)})
    counter = Counter(display.values())
    blocks_remaining = counter[BLOCK]
    pos = {val: key for key, val in display.items()}
    ball, paddle = pos[BALL], pos[PADDLE]
    score = display[(-1, 0)]
    if verbose:
        print(score)
        display.pop((-1, 0))
        printer.printdict(display)
        display[(-1, 0)] = score
    return ball, paddle, score, blocks_remaining


@blitzen.run
def main(input_string, verbose=False):
    game = [int(i) for i in input_string.split(',')]
    arcade = Intcode(game)
    arcade.prgm[0] = 2
    arcade.run(0)
    output = arcade.output
    display = {}
    (bx, by), (px, py), score, blocks_remaining = render(output, display, verbose)
    p1 = blocks_remaining
    while blocks_remaining > 0:
        if px > bx:
            joystick = -1
        elif px < bx:
            joystick = 1
        else:
            joystick = 0
        arcade.run(joystick)
        (bx, by), (px, py), score, blocks_remaining = render(output, display, verbose)
    p2 = score
    return p1, p2

