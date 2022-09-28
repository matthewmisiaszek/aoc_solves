import dancer


class Cart:
    def __init__(self, order=3):
        self.order = order  # number of axes / dimensions
        self.zero = (0,) * self.order  # origin
        self.axes = {tuple(int(j == axis) for j in range(self.order)) for axis in range(self.order)}  # positive axes
        self.neg_axes = {opposite(axis) for axis in self.axes}  # negative axes
        self.cards = self.axes | self.neg_axes  # cardinal directions
        # self.components is all directions that can be created by summing directions in self.cards
        # and a set of the cardinal directions that created them
        self.components = {self.zero: set()}
        for _ in range(self.order):
            for direction, components in tuple(self.components.items()):
                opp_components = {opposite(component) for component in components}
                for b in self.cards - components - opp_components:
                    new_direction = offset(direction, b)
                    self.components[new_direction] = components | {b}
        self.components.pop(self.zero)
        self.directions = set(self.components.keys())  # just the directions
        # directions with n components
        self.eq_ord_dirs = [{direction for direction, components in self.components.items()
                             if len(components) == order} for order in range(self.order + 1)]
        # directions with up to n components
        self.leq_ord_dirs = [{direction for direction, components in self.components.items()
                              if len(components) <= order} for order in range(self.order + 1)]
        self.opposites = {direction: opposite(direction) for direction in self.components.keys()}

    def adj(self, loc, order=1, exact_order=False):
        if exact_order is True:
            return {offset(loc, direction) for direction in self.eq_ord_dirs[order]}
        else:
            return {offset(loc, direction) for direction in self.leq_ord_dirs[order]}


def get_k(norm, loc):
    return sum([a * b for a, b in zip(norm, loc)])


def manhattan(a, b=None):
    if b is None:
        b = (0,) * len(a)
    return sum([abs(ai - bi) for ai, bi in zip(a, b)])


def offset(loc, direction, multiple=1):
    return tuple(a + b * multiple for a, b in zip(loc, direction))


def opposite(direction):
    return tuple(-i for i in direction)


def bounds(a, order):
    return tuple(tuple(fun(a, key=lambda x: x[o])[o] for fun in (min, max)) for o in range(order))
