import blitzen
from collections import Counter


def evolve(n):
    r = n * 64
    n = n ^ r  # mix
    n %= 16777216  # prune
    r = n // 32
    n = n ^ r  # mix
    n %= 16777216  # prune
    r = n * 2048
    n = n ^ r  # mix
    n %= 16777216  # prune
    return n


@blitzen.run
def main(input_string, verbose=False):
    p1 = 0
    banana_counter = Counter()
    for secret in input_string.split('\n'):
        secret = int(secret)
        seq = (None,) * 4
        last = secret % 10
        seen = set()
        for _ in range(2000):
            secret = evolve(secret)
            nlast = secret % 10
            seq = seq[1:] + (nlast - last,)
            if seq not in seen:
                banana_counter.update({seq: nlast})
                seen.add(seq)
            last = nlast
        p1 += secret
    p2 = max(banana_counter.values())
    return p1, p2
