import blitzen
import re
from donner import spatial

def rintersect(r1, r2):
    ret = tuple(min(a, b) for a, b in zip(r1, r2))
    a, b, c, d = ret
    if a-b<=0 or c-d<=0:
        return False
    return ret


def makeregion(sensor, beacon):
    mh = sensor.manhattan(beacon)
    mp = spatial.Point(mh, 0)
    x1 = sensor.x - mh
    x2 = sensor.x + mh
    y = sensor.y
    b1 = y-x1
    b2 = x2 - y
    b3 = y+x2
    b4 = -y-x1
    return (b1, b2), (b3, b4)

TARGET = 2000000
grid1 = 4000000
# grid1 = 20
grid2 = 4000000

@blitzen.run
def main(input_string, verbose=False):
    inrange = set()
    beacons = set()
    regions = set()
    ups = set()
    downs = set()
    p1 = set()
    for group in re.findall('Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)', input_string):
        sx, sy, bx, by = (int(i) for i in group)
        sensor = spatial.Point(sx, sy)
        beacon = spatial.Point(bx, by)
        mh = sensor.manhattan(beacon)
        regions.add((sensor, mh))
        n = mh - abs(sensor.y - TARGET)
        if abs(sensor.y-TARGET)<=mh:
            for x in range(sensor.x - n, sensor.x+n+1):
                p1.add(x)
        if beacon.y ==TARGET:
            beacons.add(beacon.x)
        up, down = makeregion(sensor, beacon)
        ups.add(up)
        downs.add(down)

    print(sorted(ups))
    print(sorted(downs))
    p1 = len(p1-beacons)
    p2 = 1
    return p1, p2
#2825078
