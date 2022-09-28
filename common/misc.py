import DANCER
import hashlib


def combinations(items, length, duplicates=False):
    items_len = len(items)
    not_duplicates = not duplicates
    if duplicates is True:
        idxs = [0] * length
        limits = (items_len-1,) * length
    else:
        idxs = list(range(length))
        limits = tuple(items_len - length + idx for idx in idxs)
    combo = [items[i] for i in idxs]
    yield tuple(combo)
    while True:
        for i in reversed(range(length)):
            if idxs[i] < limits[i]:
                break
        else:
            return
        idxs[i] += 1
        combo[i] = items[idxs[i]]
        for j in range(i + 1, length):
            idxs[j] = idxs[j - 1] + not_duplicates
            combo[j] = items[idxs[j]]
        yield tuple(combo)


def permutations(plist):
    ret = []
    for combo in plist:
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


def digits(n, base=10, power=None):
    if isinstance(n, list) or isinstance(n, tuple):
        return sum([n[i] * base ** (len(n) - i - 1) for i in range(len(n))])
    else:
        if power is None:
            power = roughlog(n, base)
        else:
            power -= 1
        ret = []
        for i in range(power+1):
            ret.append(n // base ** (power - i))
            n %= base ** (power - i)
        return tuple(ret)

aoc_input = False

if __name__ == "__main__":
    import sys

    sys.path.append('..')