import time
start = time.time()


import numpy as np

class ScanClass:
    def __init__(self, scanner):
        scanner = scanner.split('\n')
        self.id = int(scanner[0].split()[2])
        beacons = tuple(tuple(int(i) for i in point.split(',')) for point in scanner[1:])
        self.comp = set()  # scanners this scanner has been compared to
        self.position = False  # scanner position, False if unknown
        self.beacons = beacons
        self.set_triangles()

    def set_triangles(self):
        lines = {}
        for ai in range(len(self.beacons)):
            a = self.beacons[ai]
            for bi in range(ai+1,len(self.beacons)):
                b = self.beacons[bi]
                lines[(ai, bi)] = sum([(ai - bi) ** 2 for ai, bi in zip(a,b)]) ** .5
        self.triangles = {}
        for ai in range(len(self.beacons)):
            for bi in range(ai+1,len(self.beacons)):
                for ci in range(bi+1, len(self.beacons)):
                    sides = [lines[(ai, bi)], lines[(bi, ci)], lines[(ai, ci)]]
                    corners = [ci,ai, bi]
                    while not sides[0] == min(sides):
                        sides = sides[1:] + [sides[0]]
                        corners = corners[1:] + [corners[0]]
                    if sides[1] > sides[2]:
                        sides = [sides[0], sides[2], sides[1]]
                        corners = [corners[0], corners[2], corners[1]]
                    if len(sides)==len(set(sides)):
                        self.triangles[tuple(sides)]=tuple(corners)

    def match_beacon(self,other_beacon):
        my_triangles = set(self.triangles.keys())
        other_triangles = set(other_beacon.triangles.keys())
        match_triangles = list(my_triangles.intersection(other_triangles))
        if match_triangles:
            match_triangle = match_triangles[0]
            m = np.array([np.array(self.beacons[i]) for i in self.triangles[match_triangle]])
            o = np.array([np.array(other_beacon.beacons[i]) for i in other_beacon.triangles[match_triangle]])
            mavg = m[0]+(m[1]-m[0])/np.abs(m[1]-m[0]).astype(int)
            oavg = o[0]+(o[1]-o[0])/np.abs(o[1]-o[0]).astype(int)
            A = np.round(np.linalg.solve((m-mavg), (o-oavg)),0).astype(int)
            self.beacons = [tuple((beacon-mavg)@A + oavg) for beacon in self.beacons]
            self.position = mavg@A-oavg
            return True
        else:
            return False


def main(input_file='input.txt', verbose=False):
    scanraw = open(input_file).read().split('\n\n')
    scanners = [ScanClass(scanner) for scanner in scanraw]
    scanners[0].position = (0,0,0)
    matched = set([0])
    while len(matched)<len(scanners):
        for i in range(len(scanners)):
            if i not in matched:
                for j in matched:
                    if scanners[i].match_beacon(scanners[j]):
                        matched.add(i)
                        break
    beacons = set()
    maxman=0
    for scanner in scanners:
        beacons = beacons.union(set(scanner.beacons))
        for scanner2 in scanners:
            man = sum(abs(ai-bi) for ai,bi in zip(scanner.position, scanner2.position))
            maxman = max(maxman, man)
    p1 = len(beacons)
    p2 = maxman

    if verbose:
        print('\nAll scanners placed.')
        print('Part1: ', p1)
        print('Part2: ', p2)
    return p1, p2


if __name__ == "__main__":
    main(verbose=True)
    print('elapsed time: ',time.time()-start)
