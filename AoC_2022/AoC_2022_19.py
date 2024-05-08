import blitzen
import re
from collections import defaultdict
import math

ORE = 'ore'
GEODE = 'geode'


def esum(a, b):
    return tuple(ai + bi for ai, bi in zip(a, b))


def ediff(a, b):
    return tuple(ai - bi for ai, bi in zip(a, b))

def emulsum(a, b, c):
    return tuple(ai + bi * c for ai, bi in zip(a, b))


def most_geodes_flat(blueprint, types, time):
    geode_index = types.index(GEODE)
    max_rate = [max(recipe[i] for _, recipe in blueprint) for i in range(len(types))]
    max_rate[geode_index] = sum(range(time))  # semi-arbitrary big number
    robots = tuple(int(t == ORE) for t in types)
    resources = (0,) * len(types)
    stack = [(robots, resources, time)]
    closed = set()
    most = 0
    while stack:
        curr = stack.pop()
        if curr in closed:
            continue
        closed.add(curr)
        robots, resources, time = curr
        eventual_geodes = resources[geode_index] + robots[geode_index] * time
        if eventual_geodes > most:
            most = eventual_geodes
        if time <= 0:
            continue
        optimistic_geodes = resources[geode_index] + robots[geode_index] * time + time * (time - 1) // 2
        if optimistic_geodes <= most:
            continue
        for product, recipe in blueprint:
            # don't make more robots when we already have enough
            i = product.index(1)  # the robot we're considering
            robi = robots[i]  # how many we currently have
            resi = resources[i]  # current stock of that resource
            mqi = max_rate[i]  # max consumption rate of that resource
            if (mqi - robi) * time - resi <= 0:  # if we already have enough then don't bother
                continue
            # how long do we have to wait to make this robot?
            etime = 0
            for rob, res, rec in zip(robots, resources, recipe):
                if rec - res > 0:
                    if rob == 0:
                        etime = -1
                        break
                    etime = max(etime, math.ceil((rec - res) / rob))
            # if we'll never make the robot or won't make it in time, don't bother
            if etime < 0 or etime >= time:
                continue
            nrobots = esum(robots, product)  # make the robot
            nresources = ediff(resources, recipe)  # subtract the cost
            nresources = emulsum(nresources, robots, etime + 1)  # grind
            stack.append((nrobots, nresources, time - etime - 1))  # push
    return most


def parse(input_string):
    blueprints = []
    bp_pattern = r'Blueprint (?P<BPN>\d+):(?P<recipes>(?:\s*Each \S+ robot costs (?:\d+ \S+(?: and )?)+.)+)'
    r_pattern = r'Each (?P<product>\S+) robot costs (?P<ingredients>(?:\d+ \S+(?: and )?)+)\.'
    ing_pattern = r'(?P<qty>\d+) (?P<ing>\S+)'
    types = set()
    for bpn, recipes in re.findall(bp_pattern, input_string):
        # create blueprints as [(number, {product:{ingredient:quantity}})]
        # create set of all types
        bpn = int(bpn)
        blueprint = {}
        blueprints.append((bpn, blueprint))
        for product, ingredients in re.findall(r_pattern, recipes):
            blueprint[product] = defaultdict(int)
            types.add(product)
            for qty, ing in re.findall(ing_pattern, ingredients):
                blueprint[product][ing] = int(qty)
                types.add(ing)
    types = tuple(types)
    # convert blueprints to [(number, ((product, recipe),))]
    # where product and recipe are tuples representing the amount of each type produced and consumed
    for i, (bpn, blueprint) in enumerate(blueprints):
        nblueprint = []
        for ptype in types:
            product = tuple(int(ptype == t) for t in types)
            recipe = tuple(blueprint[ptype][itype] for itype in types)
            nblueprint.append((product, recipe))
        nblueprint = tuple(nblueprint)
        blueprints[i] = (bpn, nblueprint)
    robots = tuple(1 if t == ORE else 0 for t in types)  # start with 1 ore robot
    resources = tuple(0 for _ in types)  # start with no resources
    geode_index = types.index(GEODE)  # the index where geode is stored since it's somewhat random
    return blueprints, robots, resources, geode_index, types


@blitzen.run
def main(input_string, verbose=False):
    blueprints, robots, resources, geode_index, types = parse(input_string)
    p1 = 0
    for bpn, blueprint in blueprints:
        maxqty = [max(recipe[i] for _, recipe in blueprint) for i in range(len(resources))]
        maxqty[geode_index] = 1000000
        p1 += bpn * most_geodes_flat(blueprint, types, 24)
    p2 = 1
    for bpn, blueprint in blueprints[:3]:
        p2 *= most_geodes_flat(blueprint, types, 32)
    return p1, p2

