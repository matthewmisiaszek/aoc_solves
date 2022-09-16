def esum(a, b):
    return tuple(ai + bi for ai, bi in zip(a, b))


def ediff(a, b):
    return tuple(ai - bi for ai, bi in zip(a, b))


def eprod(a, b):
    return tuple(ai * bi for ai, bi in zip(a, b))


def ediv(a, b):
    return tuple(ai / bi for ai, bi in zip(a, b))


def efloor(a, b):
    return tuple(ai // bi for ai, bi in zip(a, b))


def emod(a, b):
    return tuple(ai % bi for ai, bi in zip(a, b))


def eabs(a):
    return tuple(abs(ai) for ai in a)


def epwr(a, p=2):
    return tuple(ai ** p for ai in a)


def eabsdiff(a, b):
    return tuple(abs(ai - bi) for ai, bi in zip(a, b))


def emulsum(a, b, m):
    return tuple(ai + bi * m for ai, bi in zip(a, b))


def sum2d(a, b, m=1):
    return a[0] + b[0] * m, a[1] + b[1] * m


def sum3d(a, b, m=1):
    return a[0] + b[0] * m, a[1] + b[1] * m, a[2] + b[2] * m


def prod(a):
    ret=1
    for ai in a:
        ret*=ai
    return ret