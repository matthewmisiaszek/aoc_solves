import dancer
import re
from common import printer


def main(input_string, verbose=False):

    points = re.findall('position=<(.*)> velocity=<(.*)>', input_string)
    points = [[[int(i) for i in group.split(',')] for group in line] for line in points]
    points = sorted(points, key=lambda x: x[0][1])
    (px1, py1), (vx1, vy1) = points[0]
    (px2, py2), (vx2, vy2) = points[-1]
    t = (py1 - py2) // (vy2 - vy1)
    points2 = {(px + vx * t, py + vy * t) for (px, py), (vx, vy) in points}
    message = printer.strset(points2)
    return message, t

if __name__ == "__main__":
    dancer.run(main, year=2018, day=10, verbose=True)