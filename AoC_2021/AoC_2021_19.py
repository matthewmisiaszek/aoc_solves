import numpy as np
import blitzen


class ScanClass:
    def __init__(self, scanner):
        self.triangles = None
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
            for bi in range(ai + 1, len(self.beacons)):
                b = self.beacons[bi]
                lines[(ai, bi)] = sum(np.subtract(a, b) ** 2) ** .5
        self.triangles = {}
        for ai in range(len(self.beacons)):
            for bi in range(ai + 1, len(self.beacons)):
                for ci in range(bi + 1, len(self.beacons)):
                    sides = [lines[(ai, bi)], lines[(bi, ci)], lines[(ai, ci)]]
                    corners = [ci, ai, bi]
                    while not sides[0] == min(sides):
                        sides = sides[1:] + [sides[0]]
                        corners = corners[1:] + [corners[0]]
                    if sides[1] > sides[2]:
                        sides = [sides[0], sides[2], sides[1]]
                        corners = [corners[0], corners[2], corners[1]]
                    if len(sides) == len(set(sides)):
                        self.triangles[tuple(sides)] = tuple(corners)

    def match_scanner(self, other_scanner):
        my_triangles = set(self.triangles.keys())
        other_triangles = set(other_scanner.triangles.keys())
        match_triangles = list(my_triangles.intersection(other_triangles))
        if match_triangles:
            match_triangle = match_triangles[0]
            matrices, offsets = [], []
            for scanner in (self, other_scanner):
                a, b, c = [scanner.beacons[i] for i in scanner.triangles[match_triangle]]
                b, c = [np.subtract(i, a) for i in (b, c)]
                d = np.cross(b, c)
                matrices.append((b, c, d))
                offsets.append(a)
            A = np.round(np.linalg.solve(*matrices), 0).astype(int)
            O = offsets[0] @ A - offsets[1]
            self.beacons = [tuple(beacon @ A - O) for beacon in self.beacons]
            self.position = O
            return True
        else:
            return False


def main(input_string, verbose=False):
    scanraw = input_string.split('\n\n')
    scanners = [ScanClass(scanner) for scanner in scanraw]
    scanners[0].position = (0, 0, 0)
    matched = {0}
    while len(matched) < len(scanners):
        for i in range(len(scanners)):
            if i not in matched:
                for j in matched:
                    if scanners[i].match_scanner(scanners[j]):
                        matched.add(i)
                        break
    beacons = set()
    maxman = 0
    for scanner in scanners:
        beacons = beacons.union(set(scanner.beacons))
        for scanner2 in scanners:
            man = int(sum(abs(ai - bi) for ai, bi in zip(scanner.position, scanner2.position)))
            maxman = max(maxman, man)
    p1 = len(beacons)
    p2 = maxman

    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2021, day=19, verbose=True)

