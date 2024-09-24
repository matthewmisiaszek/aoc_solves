import blitzen
from donner.ranges import CompoundRange


def apply_maps(maps, seeds):
    for m in maps:
        new_seeds = CompoundRange()
        for r, i in m:
            new_seeds |= (seeds & r).increment(i)
            seeds = seeds - r
        seeds |= new_seeds
    return seeds


@blitzen.run
def main(input_string, verbose=False):
    maps = input_string.split('\n\n')
    seeds = maps.pop(0)
    seeds = [int(i) for i in seeds.split()[1:]]
    seeds1 = CompoundRange(*((i, i+1) for i in seeds))
    seeds2 = CompoundRange(*((a, a + b) for a, b in zip(seeds[::2], seeds[1::2])))
    maps = [[[int(i) for i in r.split()] for r in m.split('\n')[1:]] for m in maps]
    maps = [[(CompoundRange((b, b + c)), a - b) for a, b, c in m] for m in maps]
    p1 = min(min(apply_maps(maps, seeds1)))
    p2 = min(min(apply_maps(maps, seeds2)))
    return p1, p2
