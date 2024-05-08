import blitzen
from collections import Counter


@blitzen.run
def main(input_string, verbose=False):
    points = tuple(tuple(int(i) for i in line.split(',')) for line in input_string.split('\n'))
    (xn, xx), (yn, yx) = ((fun(points, key=lambda x: x[ax])[ax]
                           for fun in (min, max))
                          for ax in (0, 1))
    distances = tuple(tuple(abs(x - px) + abs(y - py)
                            for px, py in points)
                      for x in range(xn, xx + 1)
                      for y in range(yn, yx + 1))
    mindist = tuple(min(d) for d in distances)
    mincount = tuple(d.count(m) for d, m in zip(distances, mindist))
    mindex = tuple(d.index(m) for d, m, c in zip(distances, mindist, mincount) if c == 1)
    idxcount = Counter(mindex)
    p1 = max(idxcount.values())
    sumdist = tuple(sum(x) for x in distances)
    p2 = sum((x < 10000 for x in sumdist))
    return p1, p2

