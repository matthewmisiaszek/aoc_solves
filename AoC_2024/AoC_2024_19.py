import blitzen
from collections import Counter


@blitzen.run
def main(input_string, verbose=False):
    p1 = p2 = 0
    t, d = input_string.split('\n\n')
    t = t.split(', ')
    for e, di in enumerate(d.split('\n')):
        q = Counter((di,))
        combos = 0
        while q:
            c = max(q.keys(), key=lambda x: len(x))
            f = q.pop(c)
            for ti in t:
                if ti == c[:len(ti)]:
                    if len(ti) == len(c):
                        combos += f
                    else:
                        q.update({c[len(ti):]: f})
        p1 += combos > 0
        p2 += combos
    return p1, p2
