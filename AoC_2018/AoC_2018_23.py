# Conventions:
# North is +Y, East is +X, Up is +Z
# Coordinate tuples are in (x,y,z) order
# Plane equation ax+by+cz=k is used (slightly different from ax+by+cz+k=0)
# A plane can then be described as a normal vector (a,b,c) and a k value
# The range of a bot is called a region
# Intersections of regions are also regions
# A region has 8 sides: North-East-Up, North-West-Up, South-West-Up, South-East-Up and 4 corresponding down directions
# for brevity, N: North, S: South, W: West, E: East, U: Up, D: Down
# For convenience, down/bottom sides use the same normal vector as the parallel up/top side
# example: NEU is parallel to SWD so both planes can be described with the NEU vector
# A region then is a dict with 4 keys (NE, NW, SE, SW).  Each key has a k value for the down side and up side.
# {'NE':(SWD,NEU),'NW':(SED,NWU),'SW':(NED, SWU),'SE':(NWD, SEU)
# The (D,U) pair serves as a range along the relevant vector that is 'in-range' of the bot(s)
# A cluster is a collection of bots that share one or more points 'in-range'

import blitzen
import re


def norms_constant():
    return {'NE': ( 1,  1,  1),
            'NW': (-1,  1,  1),
            'SW': (-1, -1,  1),
            'SE': ( 1, -1,  1)}


def manhattan(a, b):
    # return the manhattan distance between two points
    return sum([abs(ai - bi) for ai, bi in zip(a, b)])


def get_k(norm, loc):
    # using the plane equation a*x + b*y + c*z = k
    # find the value of k for a plane normal to vector norm (a,b,c)
    # and intersecting the point loc (x,y,z)
    x, y, z = loc
    a, b, c = norm
    return a * x + b * y + c * z


def bot_region(loc, rad):
    # return a dict (length 4) of tuples (length 2) describing the planes bounding a bot's range
    # each length 2 tuple is the max and min k value bounding the range in the respective normal direction
    # norms is a length 4 dict of the 4 normal directions as length 3 tuples
    norms = norms_constant()
    x, y, z = loc
    return {direction: tuple(get_k(norm, (x, y, zi)) for zi in (z - rad, z + rad)) for direction, norm in norms.items()}


def intersect_range(a, b):
    # find the intersection of two ranges along an axis.
    # each range should be a length 2 tuple describing min and max for the range
    an, ax = a
    bn, bx = b
    nn = max(an, bn)
    nx = min(ax, bx)
    return nn, nx


def intersect_region(a, b):
    # find the intersection of two regions by intersecting all 4 ranges defining them
    return {d: intersect_range(a[d], b[d]) for d in a.keys()}


def not_negative(region):
    # check if any of the axes in a region is negative,
    # indicating that the region has a negative volume and doesn't exist
    for n, x in region.values():
        if n > x:
            return False
    return True


def intersect_planes(planea, planeb):
    # find the slope, m and y intercept, b of the line intersection of two planes
    # don't know what this'll do if the intersection line isn't parallel to the z plane
    (aa, ba, ca), ka = planea
    (ab, bb, cb), kb = planeb
    m = (aa // ca - ab // cb) // (bb // cb - ba // ca)
    b = -(ka // ca - kb // cb) // (bb // cb - ba // ca)
    return m, b


def intersect_lines(line1, line2):
    # find the x,y point where two lines described as (m,b) tuples intersect
    m1, b1 = line1
    m2, b2 = line2
    x = (b2 - b1) // (m1 - m2)
    y = m1 * x + b1
    return x, y


def get_ys(lines, x):
    # return the y value for all lines at point x
    return tuple(m * x + b for m, b in lines)


def get_zs(planes, x, y):
    # return the z value for all planes in planes at point (x,y)
    return tuple(-(a * x + b * y - k) // c for (a, b, c), k in planes)


def get_points(region):
    # return a set of all points bounded by a region
    norms = norms_constant()
    solutions = set()
    # {direction: (norm, k value)} for all top (+z) bounding planes
    top_planes = {key: (norms[key], region[key][1]) for key in norms.keys()}
    # translate keys for top planes to keys for bottom planes
    # the bottom plane corresponding to a top plane has opposite x and y normal vector
    # example: top plane NE (1,1,1) corresponds to bottom plane SW (-1,-1,1)
    norms_inv = {value: key for key, value in norms.items()}
    rekey = {norms_inv[(-x, -y, z)]: norms_inv[(x, y, z)] for x, y, z in norms_inv.keys()}
    # {direction: (norm, k value)} for all bottom (-z) bounding planes
    bottom_planes = {rekey[key]: (norms[key], region[key][0]) for key in norms.keys()}
    # find the lines where top and bottom planes intersect for each direction (key)
    lines = {key: intersect_planes(top_planes[key], bottom_planes[key]) for key in norms.keys()}
    # organize lines by which intersection point they create (N, S, E, or W)
    direction_lines = {d: {key: value for key, value in lines.items() if key.find(d) >= 0} for d in 'NSEW'}
    # find the min and max x values from lines (West and East intersections)
    xmin, xmax = tuple(intersect_lines(*direction_lines[d].values())[0] for d in ('W', 'E'))
    # iterate from min to max x
    for x in range(xmin, xmax + 1):
        # y min bound is max value of all South lines at point x
        ymin = max(get_ys(direction_lines['S'].values(), x))
        # y max bound is min value of all North lines at point x
        ymax = min(get_ys(direction_lines['N'].values(), x))
        for y in range(ymin, ymax + 1):
            # max z value is min of all top planes at point (x,y)
            maxz = min(get_zs(top_planes.values(), x, y))
            # min z value is max of all bottom planes at point (x,y)
            minz = max(get_zs(bottom_planes.values(), x, y))
            for z in range(minz, maxz + 1):
                # record point x,y,z to return variable
                solutions.add((x, y, z))
    return solutions


def parse(input_string):
    f = input_string
    raw_re = re.findall('pos=<(.*),(.*),(.*)>, r=(.*)', f)
    int_re = [[int(i) for i in group] for group in raw_re]
    return tuple((r, (x, y, z), i) for i, (x, y, z, r) in enumerate(int_re))


def part1(bots):
    radius, strongest, idx = max(bots)
    return sum([manhattan(strongest, loc) <= radius for r, loc, i in bots])


def part2(bots):
    # sort by size then reading order
    # Big bots are more likely to be part of the biggest cluster
    # This may also mitigate confounding / distracting bots
    bots = sorted(bots)
    # convert bots from point, radius to regions
    botregions = tuple((i, bot_region(loc, r)) for r, loc, i in bots)
    # set of all bot indices for use later
    all_bots = set(range(len(botregions)))
    open_seeds = {0}  # queue variable / seeds we want to try
    closed_seeds = {}  # seeds we've already tried
    biggest_cluster = 0  # the number of bots in the biggest cluster so far
    while open_seeds:
        seed = open_seeds.pop()  # working seed
        _, cluster = botregions[seed]  # working cluster
        bots = {seed}  # set of indices of the bots in this cluster
        for idx, bot in botregions[seed + 1:] + botregions[:seed]:  # start from seed in hopes of preventing confounding
            new_region = intersect_region(cluster, bot)
            # if this bot intersects the current cluster, add it to the cluster
            if not_negative(new_region):
                bots.add(idx)
                cluster = new_region
        # record the cluster this seed produced
        closed_seeds[seed] = (len(bots), cluster)
        # if it's the biggest cluster so far,
        # we should check the bots that weren't in it to try and find even bigger clusters
        # but don't try seeds we've already tried.  That would be silly.
        if len(bots) > biggest_cluster:
            biggest_cluster = len(bots)
            excluded_bots = all_bots - bots
            open_seeds.update(excluded_bots - closed_seeds.keys())
    # filter clusters for size
    clusters = tuple(cluster for size, cluster in closed_seeds.values() if size == biggest_cluster)
    # find all points from all largest clusters
    solutions = set().union(*[get_points(cluster) for cluster in clusters])
    solution_manhattans = {manhattan((0, 0, 0), solution) for solution in solutions}
    return min(solution_manhattans)


def main(input_string, verbose=False):
    bots = parse(input_string)
    p1 = part1(bots)
    p2 = part2(bots)
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2018, day=23, verbose=True)
