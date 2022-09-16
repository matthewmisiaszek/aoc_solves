import hashlib


def combinations(inlist, maxl=None, minl=0):
    if maxl is None:
        maxl = len(inlist)
    stop = 2 ** len(inlist)
    masks = tuple(digits(i, 2) for i in range(stop))
    masks = tuple(mask for mask in masks if minl <= sum(mask) <= maxl)
    return sorted((tuple(li for li, mi in zip(inlist, mask) if mi) for mask in masks), key=len)


def permutations(plist, maxl=-1, minl=0):
    combos = combinations(plist, maxl, minl)
    ret = []
    for combo in combos:
        n = len(combo)
        c = []
        for i in range(n):
            c.append(0)
        ret.append(tuple(combo))
        combo = list(combo)
        i = 0
        while i < n:
            if c[i] < i:
                if i % 2 == 0:
                    temp = combo[0]
                    combo[0] = combo[i]
                    combo[i] = temp
                else:
                    temp = combo[c[i]]
                    combo[c[i]] = combo[i]
                    combo[i] = temp
                ret.append(tuple(combo))
                c[i] += 1
                i = 0
            else:
                c[i] = 0
                i += 1
    return tuple(ret)


def md5hash(seed):
    # md5 hash as commonly implemented in AoC
    return hashlib.md5(seed.encode('utf-8')).hexdigest()


def CRT(n, b):
    # Chinese Remainder Theorem
    # n is the period of each gate
    # b is n-current position-distance from start
    N = 1
    for ni in n:
        N *= ni
    Ni = [N // ni for ni in n]
    ret = 0
    for i in range(len(n)):
        xi = 0
        while (Ni[i] * xi) % n[i] != 1:
            xi += 1
        ret += Ni[i] * xi * b[i]
    return ret % N


def roughlog(x, b):
    ret = 0
    while x >= b:
        ret += 1
        x /= b
    return ret


def digits(n, base=10):
    if isinstance(n, list) or isinstance(n, tuple):
        return sum([n[i] * base ** (len(n) - i - 1) for i in range(len(n))])
    elif n == 0:
        return [0]
    else:
        power = roughlog(n, base)
        ret = []
        for i in range(power + 1):
            ret.append(n // base ** (power - i))
            n %= base ** (power - i)
        return tuple(ret)


if __name__ == "__main__":
    import sys

    sys.path.append('..')
