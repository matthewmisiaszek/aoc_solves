import dancer
import re
from common import printer, spatial


def main(input_string, verbose=False):

    points = re.findall('position=<(.*)> velocity=<(.*)>', input_string)
    points = [[spatial.Point([int(i) for i in group.split(',')]) for group in line] for line in points]
    p1, v1 = max(points)
    p2, v2 = min(points)
    t = (p1.y - p2.y) // (v2.y - v1.y)
    points2 = {p + v * t for p, v in points}
    message = printer.strset(points2)
    return message, t


if __name__ == "__main__":
    dancer.run(main, year=2018, day=10, verbose=True)