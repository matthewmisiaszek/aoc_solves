import blitzen


def intersect(a, b):
    an, ax = a
    bn, bx = b
    cn = max(an, bn)
    cx = min(ax, bx)
    if cn >= cx:
        return False, []
    else:
        c = (cn, cx)
    remainder = []
    if an < bn <= ax:
        remainder.append((an, bn))
    if ax > bx >= an:
        remainder.append((bx, ax))
    return c, remainder


def main(input_string, verbose=False):
    # Part 1
    maps = input_string.split('\n\n')
    seeds = maps[0]
    maps = maps[1:]
    seeds = [int(i) for i in seeds.split()[1:]]
    for map in maps:
        ranges = map.split('\n')[1:]
        ranges = [[int(i) for i in r.split()] for r in ranges]
        for i in range(len(seeds)):
            for a, b, c in ranges:
                if b <= seeds[i] < b + c:
                    seeds[i] += a-b
                    break
    p1 = min(seeds)
    # Part 2
    maps = input_string.split('\n\n')
    seeds = maps[0]
    maps = maps[1:]
    seeds = [int(i) for i in seeds.split()[1:]]
    seeds = [(a, a + b) for a, b in zip(seeds[::2], seeds[1::2])]

    for map in maps:
        ranges = map.split('\n')[1:]
        ranges = [[int(i) for i in r.split()] for r in ranges]
        ranges = [(b, b+c, a-b) for a, b, c in ranges]
        nseeds = []
        si = 0
        while si < len(seeds):
            s = seeds[si]
            for rn, rx, rp in ranges:
                r = (rn, rx)
                ns, re = intersect(s, r)
                if ns:
                    nsn, nsx = ns
                    nseeds.append((nsn+rp, nsx+rp))
                    seeds += re
                    break
            else:
                nseeds.append(s)
            si += 1
        seeds = nseeds
    p2 = min(seeds)[0]

    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2023, day=5, verbose=True)
