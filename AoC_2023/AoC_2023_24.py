import blitzen
from donner import spatial
from itertools import combinations


def ediff(a, b):
    return tuple(ai - bi for ai, bi in zip(a, b))

class HailStone:
    def __init__(self, line=None):
        pstr, vstr = line.split('@')
        self.p = spatial.Point(*(int(i) for i in pstr.split(',')))
        self.v = spatial.Point(*(int(i) for i in vstr.split(',')))
        self.m = self.v.y / self.v.x if self.v.x else None
        self.b = self.p.y - self.v.y * self.p.x / self.v.x if self.v.x else None

    def intersect2D(self, other, bounds):
        if self.m == other.m:
            return self.b == other.b
        x = (other.b - self.b) / (self.m - other.m)
        tself = (x - self.p.x) / self.v.x
        tother = (x - other.p.x) / other.v.x
        y = self.m * x + self.b
        return tself >= 0 and tother >= 0 and spatial.inbounds(spatial.Point(x, y), bounds)

    def at(self, t):
        return self.p + self.v * t

    def matrix(self):
        # equations of intersection with thrown stone for linear algebra solve
        # p(ti) = p(0) + v * ti
        # self: s, thrown stone: t
        # sp+sv*t = tp+tv*t
        # t = (tp - sp) / (sv - tv)
        # xy: t = (tpx - spx) / (svx - tvx) = (tpy - spy) / (svy - tvy)
        # (tpx - spx)(svy - tvy) = (tpy - spy)(svx - tvx)
        # tpx*svy - tpx*tpy - spx*svy + spx*tvy = tpy*svx - tpy*tvx - spy*svx + spy*tvx
        # svy*tpx - svx*tpy + 0*tpz - spy*tvx + spx*tvy + 0*tvz = spx*svy - spy*svx
        # svz*tpx + 0*tpy - svx*tpz - spz*tvx + 0*tvy + spx*tvz = spx*svz - spz*svx
        # ignore t__*t__ variables.  these cancel out when two equations are subtracted from each other.
        return ((
            (self.v.y, -self.v.x, 0, -self.p.y, self.p.x, 0, self.p.x * self.v.y - self.p.y * self.v.x),
            (self.v.z, 0, -self.v.x, -self.p.z, 0, self.p.x, self.p.x * self.v.z - self.p.z * self.v.x)
        ))


def det(a):
    # return the determinant of a
    # assumes a is square
    size = len(a)
    if size == 1:
        return a[0][0]
    ret = 0
    for i in range(size):
        sign = 1 - 2 * (i % 2)   # alternate 1, -1
        sub = list(zip(*a[1:]))  # remove first row and transpose
        sub.pop(i)               # remove i-th column
        sub = list(zip(*sub))    # transpose
        ret += sign * a[0][i] * det(sub)
    return ret


def cramer(a, b, i):
    # use cramer's rule to return the i-th unknown in the linear system ax=b
    # assumes the return value will be an integer
    ai = list(zip(*a))  # transpose a
    ai[i] = b           # replace column i with b
    ai = list(zip(*ai)) # transpose
    return det(ai) // det(a)


def main(input_string, verbose=False):
    stones = [HailStone(line) for line in input_string.split('\n')]
    n = 2e14
    x = 4e14
    bounds = (spatial.Point(n, n), spatial.Point(x, x))
    p1 = sum(a.intersect2D(b, bounds) for a, b in combinations(stones, 2))
    A = list(zip(*[s.matrix() for s in stones[:4]]))
    A = [ediff(Ai[0], Aij) for Ai in A for Aij in Ai[1:]]
    a = [Ai[:-1] for Ai in A]
    b = [Ai[-1] for Ai in A]
    p2 = sum(cramer(a, b, i) for i in range(3))

    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2023, day=24, verbose=True)
