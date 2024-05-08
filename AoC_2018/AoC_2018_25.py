import blitzen


def eabsdiff(a, b):
    return tuple((abs(bi - ai) for ai, bi in zip(a, b)))

def inrange(point):
    cdist = 3
    ret = set()
    queue = {tuple()}
    order = len(point)
    while queue:
        item = queue.pop()
        if len(item) == order:
            ret.add(item)
        else:
            rdist = cdist - sum(eabsdiff(item, point))
            x0 = point[len(item)]
            queue.update({item + (x,) for x in range(x0 - rdist, x0 + rdist + 1)})
    return ret


@blitzen.run
def main(input_string, verbose=False):
    f = input_string.split('\n')
    points = {tuple(int(i) for i in line.split(',')) for line in f}
    pointranges = {point: inrange(point) & points for point in points}
    constellations = 0
    while pointranges:
        point, constellation = pointranges.popitem()
        constellations += 1
        while constellation:
            point = constellation.pop()
            if point in pointranges:
                constellation.update(pointranges.pop(point))
    p1 = constellations
    p2 = blitzen.holiday_greeting
    return p1, p2

