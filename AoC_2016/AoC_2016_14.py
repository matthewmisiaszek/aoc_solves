import blitzen
from donner.misc import md5hash
from donner import multiproc
import re

THOUSAND = 1000


def stretch(seed):
    ret = seed
    for _ in range(2017):
        ret = md5hash(ret)
    return ret


def re_hash(h):
    cm = re.search(r'((.)\2\2)', h)
    if cm is not None:
        c3 = cm.group(2)
        c5 = tuple(i for _, i in re.findall(r'((.)\2\2\2\2)', h))
        return c3, c5
    else:
        return False, tuple()


def hash_and_check(start, batch_size, hashfun, salt):
    hashes = [(i, hashfun(salt + str(i))) for i in range(start, start + batch_size)]
    c35 = [(i, re_hash(h)) for i, h in hashes]
    c35 = [(i, c3, c5) for i, (c3, c5) in c35 if c3]
    return c35


def find_keys(mpc, result, keys, triples, want):
    for j, c3, c5 in result:
        if c3:
            for c in c5:
                keys.update([key for key in triples[c] if key >= j - THOUSAND])
                triples[c].clear()
                if mpc.app_limit is None and len(keys) >= want:
                    mpc.app_limit = max(max(x) for x in triples.values() if x) + THOUSAND
            triples[c3].add(j)


def generate(salt, hashfun, want):
    keys = set()
    triples = {c: set() for c in '0123456789abcdef'}
    multiproc.pool(proc_fun=hash_and_check, proc_args=(hashfun, salt),
                   post_fun=find_keys, post_args=(keys, triples, want))
    keys = tuple(sorted(keys))
    return keys[want - 1]


def main(input_string, verbose=False):
    p1 = generate(salt=input_string, hashfun=md5hash, want=64)
    p2 = generate(salt=input_string, hashfun=stretch, want=64)
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2016, day=14, verbose=True)
