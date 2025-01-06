import blitzen
from donner.misc import md5hash
import re


def stretch(seed):
    ret = seed
    for _ in range(2017):
        ret = md5hash(ret)
    return ret


def generate(salt, hashfun, want):
    keys = set()
    triples = {c: set() for c in '0123456789abcdef'}
    triple_pattern = re.compile(r'(.)\1\1')
    quint_pattern = re.compile(r'(.)\1\1\1\1')
    i = 0
    key = None
    while key is None or i <= key + 1000:
        hash = hashfun(salt + str(i))
        if match := triple_pattern.search(hash):
            for c in quint_pattern.findall(hash):
                for j in triples[c]:
                    if 0 < i - j <= 1000:
                        keys.add(j)
                        if len(keys) == want:
                            key = max(keys)
                triples[c].clear()
            triples[match.group(1)].add(i)
        i += 1
    return sorted(keys)[want-1]


@blitzen.run
def main(input_string, verbose=False):
    p1 = generate(salt=input_string, hashfun=md5hash, want=64)
    p2 = generate(salt=input_string, hashfun=stretch, want=64)
    return p1, p2

