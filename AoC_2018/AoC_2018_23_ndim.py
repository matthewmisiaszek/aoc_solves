# Conventions:
# Plane equation ax+by+cz=k is used (slightly different from ax+by+cz+k=0)
# A plane can then be described as a normal vector (a,b,c) and a k value
# The range of a bot is called a region
# Intersections of regions are also regions
# A cluster is a collection of bots that share one or more points 'in-range'

import blitzen
import donner.cartnd as cartnd
import re
import itertools
import numpy as np


def bot_region(loc, rad, cart):
    # return a dict (length 4) of tuples (length 2) describing the planes bounding a bot's range
    # each length 2 tuple is the max and min k value bounding the range in the respective normal direction
    # norms is a length 4 dict of the 4 normal directions as length 3 tuples
    ret = {}
    for direction, components in cart.components.items():
        if len(components)==cart.order:
            for offset in components:
                break
            k = cartnd.get_k(direction, cartnd.offset(loc, offset, rad))
            ret[direction] = k
    return ret



def intersect_region(a, b):
    # find the intersection of two regions by intersecting all 4 ranges defining them
    return {d: min(a[d], b[d]) for d in a.keys()}


def not_negative(region, cart):
    # check if any of the axes in a region is negative,
    # indicating that the region has a negative volume and doesn't exist
    for direction in region.keys():
        opposite = cart.opposites[direction]
        if region[direction]<=-region[opposite]:
            return False
    return True

def makepoint(position, cart):
    # add up a dict of vector:multiple pairs
    point = cart.zero
    for axis, value in position.items():
        point = cartnd.offset(point, axis, value)
    return point


def get_range(region, position, axis, cart):
    # return the min and max value that exists within the region along axis at point described by position
    opp_axis = cart.opposites[axis]
    coords = [(key, value) for key, value in position.items()]
    values = []
    for axis_i in (opp_axis, axis):
        values_i = [] # list of values where axis intersects the planes of region
        # plane groups are used to select planes for intersection
        # planes must be aligned with axis_i
        # intersecting planes must also have the same value for all axes in position.keys()
        # for 3D system (cart.order == 3):
        #   for first axis, select 1 group of 4 planes in +axis direction and in -axis direction to intersect
        #   for second axis, select 2 groups of 2 planes in +axis direction and in -axis direction
        #   for third axis, select 4 groups of 1 plane in +axis direction and in -axis direction
        plane_groups = [(axis_i,)]
        for paxis in position.keys():
            plane_groups.append((paxis, cart.opposites[paxis]))
        plane_groups = list(set(i) for i in itertools.product(*plane_groups))
        # for each plane_group, select planes that match
        # then create a matrix by adding fixed coords to planes
        # trim the matrix to cart.order to avoid over-constraining solver
        # solve for intersection point
        # multiply by axis_i to get distance along axis to intersection point
        # add to values
        for plane_group in plane_groups:
            planes = [(key, value) for key, value in region.items() if
                      cart.components[key] & plane_group == plane_group]
            matrix = coords + planes
            matrix = matrix[:cart.order]
            a, b = [[row[i] for row in matrix] for i in range(2)]
            matsolve = np.linalg.solve(a, b)
            axis_value = int(np.matmul(matsolve, axis_i))
            values_i.append(axis_value)
        # find min value (min for positive axis, max for negative axis)
        value_i = min(values_i)
        # if this axis is the opposite axis, multiply value by -1
        direction = np.dot(axis, axis_i)
        values.append(value_i*direction)
    return values


def get_points(region, cart):
    # return set of all points in region
    # iterate through all points along all axes in region
    # queue item is a "position" dictionary of axes and values
    # value is the signed integer location of the point on the axis
    # axes not in position are not yet constrained/defined
    solutions = set()
    queue = [{}]
    while queue:
        position = queue.pop()
        if len(position)==cart.order: # if position is fully defined, record the point
            solutions.add(makepoint(position, cart))
        else: # else, choose a new axis to explore, get min/max values along that axis at this position, and append
            axis = (cart.axes - position.keys()).pop()
            n,x = get_range(region, position, axis, cart)
            for val in range(n,x+1):
                nposition = position.copy()
                nposition[axis]=val
                queue.append(nposition)
    return solutions



def parse(input_file):
    cart = cartnd.Cart()
    f = input_file
    raw_re = re.findall('pos=<(.*),(.*),(.*)>, r=(.*)', f)
    int_re = [[int(i) for i in group] for group in raw_re]
    return tuple((r, (x, y, z), i) for i, (x, y, z, r) in enumerate(int_re)), cart


def part1(bots):
    radius, strongest, idx = max(bots)
    return sum([cartnd.manhattan(strongest, loc) <= radius for r, loc, i in bots])


def part2(bots, cart):
    # sort by size then reading order
    # Big bots are more likely to be part of the biggest cluster
    # This may also mitigate confounding / distracting bots
    bots = sorted(bots)
    # convert bots from point, radius to regions
    botregions = tuple((i, bot_region(loc, r, cart)) for r, loc, i in bots)
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
            if not_negative(new_region, cart):
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
    solutions = set().union(*[get_points(cluster, cart) for cluster in clusters])
    solution_manhattans = {cartnd.manhattan((0, 0, 0), solution) for solution in solutions}
    return min(solution_manhattans)


def main(input_string, verbose=False):
    bots, cart = parse(input_string)
    p1 = part1(bots)
    p2 = part2(bots, cart)
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2018, day=23, verbose=True)
