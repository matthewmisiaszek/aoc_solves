import dancer
import re
from itertools import product

XMUL = 4000000
SEARCH_RANGE = (0, 4000000)
SEARCH_ROW = 2000000


# For Example:
# SEARCH_RANGE = (0, 20)
# SEARCH_ROW = 10


def make_region(sensor, pad=0):
    # create a 2D region centered at sx, sy and containing bx, by with padding
    # region is two tuples of min max values along vectors (1,1) and (-1,1) respectively
    # +(-1,1) / \ +(1,1)
    #  -(1,1) \ / -(-1,1)
    sx, sy, bx, by = sensor
    man = abs(sx - bx) + abs(sy - by) + pad
    return (sy + sx - man, sy + sx + man), (sy - sx - man, sy - sx + man)


def center(region):
    # return the point at the center of a region
    (a, b), (c, d) = region
    e = (a + b) // 2
    f = (c + d) // 2
    x = (e - f) // 2
    y = e - x
    return x, y


def intersect_ranges(a, b):
    # return the overlapping area of two ranges of (min,max)
    an, ax = a
    bn, bx = b
    return max(an, bn), min(ax, bx)


def intersect_regions(a, b):
    # return the intersection of regions a and b by intersecting their ranges
    return tuple(intersect_ranges(ai, bi) for ai, bi in zip(a, b))


def valid_region(region):
    # check if a region is "valid" or contains any space
    # region boundaries are not included in the region so all ranges must be at least 2 wide
    for a, b in region:
        if b - a < 2:
            return False
    return True


def subtract(a, b):
    # return set of regions representing region a minus region b
    intersection = intersect_regions(a, b)
    if not valid_region(intersection):
        return {a}  # no intersection, region unchanged
    if intersection == a:
        return {}  # 100% intersection, no region remains
    aj, ak = a
    ij, ik = intersection
    nj = sorted(set(aj + ij))  # all unique boundaries along J vector, sorted
    nk = sorted(set(ak + ik))  # all unique boundaries along K vector, sorted
    new_regions = {(q, r) for q, r in product(zip(nj, nj[1:]), zip(nk, nk[1:]))}  # divide a by boundaries
    new_regions = {region for region in new_regions if valid_region(region)}
    new_regions.discard(intersection)  # remove intersection
    return new_regions


def subtract_from_all(regions, sensor):
    # subtract the region sensor from all regions in regions
    for region in tuple(regions):
        regions.discard(region)
        regions.update(subtract(region, sensor))


def part2(sensors):
    # convert all sensors to regions
    sensors = [make_region(sensor) for sensor in sensors]
    # create a region that fully contains the search area
    search_min, search_max = SEARCH_RANGE
    search_mean = (search_min + search_max) // 2
    search_region = make_region((search_mean, search_mean, search_min, search_min), pad=1)
    # subtract each sensor from the search region(s)
    regions = {search_region}
    for sensor in sensors:
        subtract_from_all(regions, sensor)
    # define the search area (with padding)
    search_area = ((search_min - 1, search_max + 1), (search_min - 1, search_max + 1))
    # check each remaining region to see if its center falls within the search area
    for region in tuple(regions):
        c = center(region)
        if all(search_min <= ci <= search_max for ci in c):
            x, y = c
            return x * XMUL + y


def part1(sensors):
    beacons = set()
    no_beacons = set()
    for sensor in sensors:
        sx, sy, bx, by = sensor
        man = abs(sx - bx) + abs(sy - by)
        xr = man - abs(sy - SEARCH_ROW)
        if xr > 0:
            for x in range(-xr, xr + 1):
                no_beacons.add(sx + x)
        if by == SEARCH_ROW:
            beacons.add(bx)
    return len(no_beacons - beacons)


def main(input_string, verbose=False):
    pattern = r'Sensor at x=(-?\d*), y=(-?\d*): closest beacon is at x=(-?\d*), y=(-?\d*)'
    sensors = [[int(i) for i in group] for group in re.findall(pattern, input_string)]
    p1 = part1(sensors)
    p2 = part2(sensors)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2022, day=15, verbose=True)
