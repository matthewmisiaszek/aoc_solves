import DANCER


def esum(a, b):
    """elementwise sum of a and b"""
    return tuple(ai + bi for ai, bi in zip(a, b))


def ediff(a, b):
    """elementwise difference of a and b"""
    return tuple(ai - bi for ai, bi in zip(a, b))


def eprod(a, b):
    """elementwise product of a and b"""
    return tuple(ai * bi for ai, bi in zip(a, b))


def ediv(a, b):
    """elementwise division of a by b"""
    return tuple(ai / bi for ai, bi in zip(a, b))


def efloor(a, b):
    """elementwise floor division of a by b"""
    return tuple(ai // bi for ai, bi in zip(a, b))


def emod(a, b):
    """elementwise modulus division of a by b"""
    return tuple(ai % bi for ai, bi in zip(a, b))


def eabs(a):
    """elementwise absolute value of a"""
    return tuple(abs(ai) for ai in a)


def epwr(a, p=2):
    """raise every element of a to the p power"""
    return tuple(ai ** p for ai in a)


def eabsdiff(a, b):
    """elementwise absolute difference of a and b"""
    return tuple(abs(ai - bi) for ai, bi in zip(a, b))


def emulsum(a, b, m):
    """elementwise (ai + bi * m) for ai, bi in zip(a, b)"""
    return tuple(ai + bi * m for ai, bi in zip(a, b))


def sum2d(a, b, m=1):
    """2D only elementwise (ai + bi * m) for ai, bi in zip(a, b)"""
    return a[0] + b[0] * m, a[1] + b[1] * m


def sum3d(a, b, m=1):
    """3D only elementwise (ai + bi * m) for ai, bi in zip(a, b)"""
    return a[0] + b[0] * m, a[1] + b[1] * m, a[2] + b[2] * m


def prod(a):
    """product of all elements in a"""
    ret = 1
    for ai in a:
        ret *= ai
    return ret
