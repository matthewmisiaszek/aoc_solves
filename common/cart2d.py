import dancer


class Direction:
    def __init__(self, name, axis, sign):
        self.axis = axis
        self.sign = sign
        self.name = name
        self.left = None
        self.right = None
        self.back = None
        self.forward = None

    def assign(self, left, right, back, forward):
        self.left = left
        self.right = right
        self.back = back
        self.forward = forward

    def move(self, point):
        if self.axis == 0:
            return point[0] + self.sign, point[1]
        else:
            return point[0], point[1] + self.sign

    def __str__(self):
        return self.name


class Cart:
    def __init__(self, transpose=False):
        if transpose:
            x=1
            y=0
        else:
            x=0
            y=1
        self.north = Direction('North', y, -1)
        self.south = Direction('South', y, 1)
        self.east = Direction('East', x, 1)
        self.west = Direction('West', x, -1)
        self.north.assign(self.west, self.east, self.south, self.north)
        self.south.assign(self.east, self.west, self.north, self.south)
        self.east.assign(self.north, self.south, self.west, self.east)
        self.west.assign(self.south, self.north, self.east, self.west)