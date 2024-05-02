import blitzen
import numpy as np


def main(input_string, verbose=False):
    points = np.array([[[int(j) for j in k]
                        for k in (i[3:-1].split(',')for i in line.split(', '))]
                       for line in input_string.split('\n')])
    p, v, a = (points[:, i, :] for i in range(3))
    p1 = list(np.lexsort([np.sum(i * np.sign(a), axis=1) for i in (p, v, a)]))[0]
    for axis in range(3):
        converged = np.lexsort([i[:, axis] for i in (p, v, a)])
        while not np.array_equiv(np.lexsort([p[:, axis]]), converged):
            v += a
            p += v
            _, i, c = np.unique(p, axis=0, return_counts=True, return_index=True)
            if max(c) > 1:
                mask = [i for c, i in zip(c, i) if c == 1]
                p = p[mask]
                v = v[mask]
                a = a[mask]
                converged = np.lexsort([i[:, axis] for i in (p, v, a)])

    p2 = p.shape[0]
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2017, day=20, verbose=True)
