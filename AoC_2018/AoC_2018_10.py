import blitzen
import re
from donner import printer, spatial


@blitzen.run
def main(input_string, verbose=False):
    points = re.findall('position=<(.*)> velocity=<(.*)>', input_string)
    points = [[spatial.Point(*[int(i) for i in group.split(',')]) for group in line] for line in points]
    y_velocities = {v.y for p, v in points}
    p1, v1 = max((p, v) for p, v in points if v.y == max(y_velocities))
    p2, v2 = max((p, v) for p, v in points if v.y == min(y_velocities))
    t = int(round((p1.y - p2.y) / (v2.y - v1.y)))
    points2 = {p + v * t for p, v in points}
    message = printer.strset(points2)
    return message, t
