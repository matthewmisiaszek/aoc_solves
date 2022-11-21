class BitSet:
    """Store set-type data in ints!  Fast, immutable, and hashable."""

    def __init__(self, keys=None):
        if keys is None:
            self.dict = {}
        else:
            self.dict = {key: 2 ** i for i, key in enumerate(keys)}

    def __repr__(self):
        return str(self.dict)

    def full_set(self):
        return 2 ** (len(self.dict)) - 1

    def add(self, bitset, item):
        if item not in self.dict:
            self.dict[item] = 2 ** len(self.dict)
        return bitset | self.dict[item]

    def discard(self, bitset, item):
        if item in self.dict:
            return bitset ^ self.dict[item]
        else:
            return bitset

    def intersect(self, *args):
        ret = self.full_set()
        for arg in args:
            ret = ret & arg
        return ret

    def difference(self, bitset, *args):
        for arg in args:
            bitset = bitset & self.complement(arg)
        return bitset

    def union(self, *args):
        ret = 0
        for arg in args:
            ret = ret | arg
        return ret

    def xor(self, *args):
        ret = 0
        for arg in args:
            ret = ret ^ arg
        return ret

    def complement(self, bitset):
        ret = self.full_set()
        return ret ^ bitset

    def to_bs(self, iterable):
        ret = 0
        for i in iterable:
            ret = self.add(ret, i)
        return ret

    def to_set(self, bitset):
        return set(self.loop(bitset))

    def isin(self, bitset, item):
        return item in self.dict and self.dict[item] & bitset == self.dict[item]

    def loop(self, bitset):
        for key, val in self.dict.items():
            if val & bitset == val:
                yield key

    def print(self, bitset):
        print('{' + ', '.join([str(key) for key in self.loop(bitset)]) + '}')
