from collections import Counter
import itertools


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
        for ai,a in enumerate(beacons):
            for bi,b in enumerate(beacons[ai+1:]):
                lines[(a,b)]=sum([(ai-bi)**2 for ai,bi in zip(a,b)])**.5
        triangles = {}
        for ai,a in enumerate(beacons):
            for bi,b in enumerate(beacons[ai+1:]):
                for ci,c in enumerate(beacons[ai+bi+1:]):
                    sides = tuple(sorted([lines[(a,b)],lines[(b,c)],lines[(a,c)]]))
                    triangles[sides]=(a,b,c)
        self.triangles = triangles





def main(input_file='input.txt', verbose=False):
    scanraw = open(input_file).read().split('\n\n')
    scanners = [ScanClass(scanner) for scanner in scanraw]
    scanners[0].position = (0, 0, 0)  # place first scanner (arbitrary)
    scanners[0].beacons = scanners[0].beacons[0]
    if verbose:
        print('Placing scanners...\n' + ''.join([str(scanner.id).center(3) for scanner in scanners]))
    while try_to_place(scanners):  # run the try function until it comes back False
        if verbose:
            print('\r' + ''.join([(' X ', '   ')[scanner.position is False] for scanner in scanners]), end='')
    p1 = len(stitch_beacons(scanners))
    p2 = max_dist(scanners)
    if verbose:
        print('\nAll scanners placed.')
        print('Part1: ', p1)
        print('Part2: ', p2)
    return p1, p2


def try_to_place(scanners):
    # Find first sanner that hasn't been placed yet
    # try every rotation set of beacons for this scanner
    # call find match scanner to find the matching scanner
    # if none found, record scanners previously checked to avoid duplicate work
    for unknown in scanners:  # this is the scanner we're trying to place
        if unknown.position is False:  # make sure it hasn't been placed yet
            for beacons in unknown.beacons:  # for each rotation set
                if find_match(unknown, beacons, scanners):
                    return True
            for known in scanners:  # mark all known scanners as checked because we just visited them
                if known.position:
                    unknown.comp.add(known.id)
    return False  # no new matches found - this means we're done.


def find_match(unknown, beacons, scanners):
    # try every known scanner not previously checked to the unknown scanner
    # run check matcch to see if it's a good match
    for known in scanners:  # this is the already placed scanner we're trying to match to
        if known.id != unknown.id and (known.id not in unknown.comp) and known.position:
            # check if we haven't already checked this scanner and it has been placed
            if check_match(unknown, beacons, known):
                return True
    return False


def check_match(unknown, beacons, known):
    # calculate distances between all combinations of two points for known and unknown scanners
    # if the same distance is recorded nmatch times, it's a match: record and return True
    nmatch = 12  # 12 beacons must match
    deltas = Counter([tuple(x2 - x1 for x1, x2 in zip(ubeacon, kbeacon))
                      for ubeacon in beacons for kbeacon in known.beacons])
    delta, count = deltas.most_common(1)[0]
    if count >= nmatch:
        newbeacons = set([tuple(b + p for b, p in zip(beacon, delta)) for beacon in beacons])
        unknown.position = delta
        unknown.beacons = newbeacons
        return True
    return False


def stitch_beacons(scanners):
    beacons = set()
    for scanner in scanners:
        beacons = beacons.union(scanner.beacons)
    return beacons


def max_dist(scanners):
    ret = 0
    for scanner1 in scanners:
        for scanner2 in scanners:
            ret = max(ret, sum([abs(s1 - s2) for s1, s2 in zip(scanner1.position, scanner2.position)]))
    return ret


if __name__ == "__main__":
    main(verbose=True)
