import blitzen
import re


def tokens(ax, ay, bx, by, px, py):
    # Equation 1: a * ax + b * bx = px
    # Equation 2: a * ay + b * by = py
    # solve for a...
    # a = (px - b * bx) / ax = (py - b * by) / ay
    # solve for b...
    # b = (px * ay - py * ax) / (ay * bx - by * ax)
    bt = (px * ay - py * ax)
    bb = (ay * bx - by * ax)
    if bt % bb == 0:
        b = bt // bb
        at = (px - b * bx)
        ab = ax
        if at % ab == 0:
            a = at // ab
            return 3 * a + b
    return 0


@blitzen.run
def main(input_string, verbose=False):
    e13 = int(1e13)
    p1 = p2 = 0
    pattern = re.compile(r'Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)')
    for ax, ay, bx, by, px, py in [[int(i) for i in match] for match in pattern.findall(input_string)]:
        p1 += tokens(ax, ay, bx, by, px, py)
        p2 += tokens(ax, ay, bx, by, px + e13, py + e13)
    return p1, p2
