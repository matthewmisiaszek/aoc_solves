import blitzen
import typing


class CompoundRange(set):
    def __init__(self, *args: typing.Tuple[int, int]):
        super().__init__(args)
        self.consolidate()

    def consolidate(self):
        old_ranges = sorted(self)
        self.clear()
        while old_ranges:
            n, x = old_ranges[0]
            if n >= x:
                raise Exception("invalid range: n > x!")
            while old_ranges and old_ranges[0][0] <= x:
                x = max(x, old_ranges[0][1])
                old_ranges.pop(0)
            self.add((n, x))

    def __copy__(self):
        return CompoundRange(*self)

    def __or__(self, other):
        ret = self.__copy__()
        ret.update(other)
        ret.consolidate()
        return ret

    def __and__(self, other):
        ret = CompoundRange()
        for sn, sx in self:
            for on, ox in other:
                nn = max(sn, on)
                nx = min(sx, ox)
                if nn < nx:
                    ret.add((nn, nx))
        ret.consolidate()
        return ret

    def __sub__(self, other):
        ret = self.__copy__()
        for on, ox in other:
            for n,x in tuple(ret):
                an, ax = max(n, on), min(x, ox)
                if ax > an:
                    ret.discard((n, x))
                    if n < on:
                        ret.add((n, on))
                    if x > ox:
                        ret.add((ox, x))
        ret.consolidate()
        return ret

    def __xor__(self, other):
        return(self | other) - (self & other)

    def increment(self, i):
        return CompoundRange(*((n + i, x + i) for n, x in self))

