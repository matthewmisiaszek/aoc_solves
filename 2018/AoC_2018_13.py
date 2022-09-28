import DANCER


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


class Intersection:
    def __init__(self, name):
        self.next = None
        self.name = name

    def assign(self, next_turn):
        self.next = next_turn

    def __str__(self):
        return self.name


class Constants:
    def __init__(self):
        self.north = Direction('North', 0, -1)
        self.south = Direction('South', 0, 1)
        self.east = Direction('East', 1, 1)
        self.west = Direction('West', 1, -1)
        self.north.assign(self.west, self.east, self.west, self.east)
        self.south.assign(self.east, self.west, self.east, self.west)
        self.east.assign(self.north, self.south, self.south, self.north)
        self.west.assign(self.south, self.north, self.north, self.south)

        self.left = Intersection('Left')
        self.right = Intersection('Right')
        self.straight = Intersection('Straight')
        self.left.assign(self.straight)
        self.straight.assign(self.right)
        self.right.assign(self.left)

        self.intersection = '+'
        self.forward = '/'
        self.back = '\\'
        self.corner_deets = {self.intersection, self.forward, self.back}
        self.cart_deets = {'v': self.south, '>': self.east, '^': self.north, '<': self.west}


def parse(input_string, C):
    f = input_string.split('\n')
    points = {(y, x): c for y, line in enumerate(f) for x, c in enumerate(line)}
    carts = {point: (C.cart_deets[c], C.left) for point, c in points.items() if c in C.cart_deets}
    corners = {point: c for point, c in points.items() if c in C.corner_deets}
    return carts, corners


def step(cart, carts, corners, crashed, C):
    direction, next_intersection = carts.pop(cart)
    cart = direction.move(cart)
    if cart in carts:
        crashed.append(cart)
        carts.pop(cart)
    else:
        if cart in corners:
            c = corners[cart]
            if c is C.intersection:
                if next_intersection is C.left:
                    direction = direction.left
                elif next_intersection is C.right:
                    direction = direction.right
                next_intersection = next_intersection.next
            elif c is C.forward:
                direction = direction.forward
            elif c is C.back:
                direction = direction.back
        carts[cart] = (direction, next_intersection)


def main(input_string, verbose=False):
    C = Constants()
    carts, corners = parse(input_string, C)
    crashed = []
    while len(carts) > 1:
        for cart in sorted(carts.keys()):
            if cart in carts:
                step(cart, carts, corners, crashed, C)
    p1 = tuple(reversed(crashed[0]))
    p2 = tuple(reversed(list(carts.keys())[0]))
    return p1, p2

if __name__ == "__main__":
    DANCER.run(main, year=2018, day=13, verbose=True)

