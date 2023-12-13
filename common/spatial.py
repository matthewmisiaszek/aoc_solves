import dancer
from common import misc


class Point:
    def __init__(self, x=0, y=0):
        if isinstance(x, Point):
            self.x = x.x
            self.y = x.y
        elif isinstance(x, list) or isinstance(x, tuple):
            self.x = x[0]
            self.y = x[1]
        else:
            self.x = x
            self.y = y

    def manhattan(self, other=None):
        if other is None:
            return abs(self.x) + abs(self.y)
        else:
            return abs(self.x - other.x) + abs(self.y - other.y)

    def transpose(self):
        return Point(self.y, self.x)

    def yinv(self):
        return Point(self.x, -self.y)

    def left(self):
        return Point(self.y, -self.x)

    def right(self):
        return Point(-self.y, self.x)

    def sign(self):
        return Point(misc.sign(self.x), misc.sign(self.y))

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, Point):
            return Point(self.x * other.x, self.y * other.y)
        else:
            return Point(self.x * other, self.y * other)

    def __lt__(self, other):
        if self.y == other.y:
            return self.x < other.x
        else:
            return self.y < other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        else:
            return False

    def __repr__(self):
        return 'x:' + str(self.x) + ',y:' + str(self.y)

    def __str__(self):
        return self.__repr__()

    def __getitem__(self, item):
        if item in {0, 'x', 'X'}:
            return self.x
        elif item in {1, 'y', 'Y'}:
            return self.y
        else:
            return None

    def __setitem__(self, key, value):
        if key in {0, 'x', 'X'}:
            self.x = value
        elif key in {1, 'y', 'Y'}:
            self.y = value


class Point3D:
    def __init__(self, x=0, y=0, z=0):
        if isinstance(x, Point):
            self.x = x.x
            self.y = x.y
            self.z = 0
        else:
            self.x = x
            self.y = y
            self.z = z

    def manhattan(self, other=None):
        if other is None:
            return abs(self.x) + abs(self.y) + abs(self.z)
        else:
            if isinstance(other, Point):
                other = Point3D(other)
            return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def __add__(self, other):
        if isinstance(other, Point):
            other = Point3D(other)
        return Point3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        if isinstance(other, Point):
            other = Point3D(other)
        return Point3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        if isinstance(other, Point):
            other = Point3D(other)
        if isinstance(other, Point3D):
            return Point3D(self.x * other.x, self.y * other.y, self.z * other.z)
        else:
            return Point3D(self.x * other, self.y * other, self.z * other)

    def __lt__(self, other):
        if isinstance(other, Point):
            other = Point3D(other)
        if self.y == other.y:
            if self.x == other.x:
                return self.z < other.z
            else:
                return self.x < other.x
        else:
            return self.y < other.y

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __eq__(self, other):
        if isinstance(other, Point3D):
            return self.x == other.x and self.y == other.y
        else:
            return False

    def __repr__(self):
        return 'x:' + str(self.x) + ',y:' + str(self.y) + ',z:' + str(self.z)

    def __str__(self):
        return self.__repr__()

    def __getitem__(self, item):
        if item in {0, 'x', 'X'}:
            return self.x
        elif item in {1, 'y', 'Y'}:
            return self.y
        elif item in {2, 'z', 'Z'}:
            return self.z
        else:
            return None

    def __setitem__(self, key, value):
        if key in {0, 'x', 'X'}:
            self.x = value
        elif key in {1, 'y', 'Y'}:
            self.y = value
        elif key in {2, 'z', 'Z'}:
            self.z = value


def bounds(points, pad=0):
    xes = [point.x for point in points]
    yes = [point.y for point in points]
    n = Point(min(xes) - pad, min(yes) - pad)
    x = Point(max(xes) + pad, max(yes) + pad)
    return n, x


def bounds3D(points, pad=0):
    xes = [point.x for point in points]
    yes = [point.y for point in points]
    zes = [point.z for point in points]
    n = Point3D(min(xes) - pad, min(yes) - pad, min(zes) - pad)
    x = Point3D(max(xes) + pad, max(yes) + pad, max(zes) + pad)
    return n, x


def inbounds(point, bound):
    n, x = bound
    return n.x <= point.x <= x.x and n.y <= point.y <= x.y


def inbounds3D(point, bound):
    n, x = bound
    return n.x <= point.x <= x.x and n.y <= point.y <= x.y and n.z <= point.z <= x.z


# Named Headings

# 2D Cartesian
EAST = Point(1, 0)
NORTH = Point(0, -1)
WEST = Point(-1, 0)
SOUTH = Point(0, 1)
UP = Point3D(0, 0, 1)
DOWN = Point3D(0, 0, -1)
NORTHEAST = NORTH + EAST
NORTHWEST = NORTH + WEST
SOUTHWEST = SOUTH + WEST
SOUTHEAST = SOUTH + EAST

NAMES_2D = {
    'E': EAST,
    'East': EAST,
    'R': EAST,
    'Right': EAST,
    '>': EAST,
    'N': NORTH,
    'North': NORTH,
    'U': NORTH,
    'Up': NORTH,
    '^': NORTH,
    'W': WEST,
    'West': WEST,
    'L': WEST,
    'Left': WEST,
    '<': WEST,
    'S': SOUTH,
    'South': SOUTH,
    'D': SOUTH,
    'Down': SOUTH,
    'v': SOUTH
}

NAMES_3D = {
    'E': EAST,
    'East': EAST,
    'R': EAST,
    'Right': EAST,
    '>': EAST,
    'N': NORTH,
    'North': NORTH,
    'U': UP,
    'Up': UP,
    '^': NORTH,
    'W': WEST,
    'West': WEST,
    'L': WEST,
    'Left': WEST,
    '<': WEST,
    'S': SOUTH,
    'South': SOUTH,
    'D': DOWN,
    'Down': DOWN,
    'v': SOUTH
}

# 2D Hex, East, Southeast
HEX_E_EAST = Point(1, 0)
HEX_E_NORTHEAST = Point(0, 1)
HEX_E_NORTHWEST = Point(-1, 1)
HEX_E_WEST = Point(-1, 0)
HEX_E_SOUTHWEST = Point(0, -1)
HEX_E_SOUTHEAST = Point(1, -1)

NAMES_HEX_E = {
    'East': HEX_E_EAST,
    'Northeast': HEX_E_NORTHEAST,
    'Northwest': HEX_E_NORTHWEST,
    'West': HEX_E_WEST,
    'Southwest': HEX_E_SOUTHWEST,
    'Southeast': HEX_E_SOUTHEAST

}

# 2D Hex, Southeast, South
HEX_S_SOUTH = Point(0, 1)
HEX_S_SOUTHEAST = Point(1, 0)
HEX_S_NORTHEAST = Point(1, -1)
HEX_S_NORTH = Point(0, -1)
HEX_S_NORTHWEST = Point(-1, 0)
HEX_S_SOUTHWEST = Point(-1, 1)

NAMES_HEX_S = {
    'South': HEX_S_SOUTH,
    'Southeast': HEX_S_SOUTHEAST,
    'Northeast': HEX_S_NORTHEAST,
    'North': HEX_S_NORTH,
    'Northwest': HEX_S_NORTHWEST,
    'Southwest': HEX_S_SOUTHWEST
}

# include upper and lower cases of all keys
for name_dict in (NAMES_2D, NAMES_3D, NAMES_HEX_E, NAMES_HEX_S):
    name_dict.update({key.upper(): val for key, val in name_dict.items()})
    name_dict.update({key.lower(): val for key, val in name_dict.items()})

# Ordered Headings
ENWS8 = (EAST, NORTHEAST, NORTH, NORTHWEST, WEST, SOUTHWEST, SOUTH, SOUTHEAST)
ENWS = ENWS8[::2]
ENWS_CORNERS = ENWS8[1::2]
D3D6 = tuple(Point3D(i) for i in ENWS) + (UP, DOWN)
D3D26 = tuple(Point3D(x, y, z)
              for x in range(-1, 2)
              for y in range(-1, 2)
              for z in range(-1, 2)
              if x != 0 or y != 0 or z != 0)
HEX_E_6 = (HEX_E_EAST, HEX_E_NORTHEAST, HEX_E_NORTHWEST, HEX_E_WEST, HEX_E_SOUTHWEST, HEX_E_SOUTHEAST)
HEX_S_6 = (HEX_S_SOUTH, HEX_S_SOUTHEAST, HEX_S_NORTHEAST, HEX_S_NORTH, HEX_S_NORTHWEST, HEX_S_SOUTHWEST)

FORWARD_CMD = {'F', 'FD', 'FORWARD'}
RIGHT_CMD = {'R', 'RIGHT', 'RT'}
LEFT_CMD = {'L', 'LEFT', 'LT'}
BACKWARD_CMD = {'B' 'BACKWARD', 'BACK'}
FORWARD = 'F'
RIGHT = 'R'
LEFT = 'L'
BACKWARD = 'B'


class Turtle:
    # Turtle is a controllable crawler.  Drive and move control position.
    # Drive will use R and L to turn while Move will use them to translate.
    # Drive returns final position, heading, and whether the position has been visited before
    # Move returns only position and visited
    # peek = True will simulate movement without actually moving the turtle
    def __init__(self, position=Point(), heading=NORTH, names=NAMES_2D, neighbors=ENWS):
        self.position = position
        self.heading = heading
        self.history = [(self.position, self.heading)]
        self.visited = {self.position}
        self.names = names
        self.neighbors_list = neighbors

    def drive(self, direction=FORWARD, multiple=1, peek=False):
        if multiple < 1:
            return self.position, self.heading, False
        direction = direction.upper()
        forward = (direction in FORWARD_CMD) - (direction in BACKWARD_CMD)
        left = direction in LEFT_CMD
        right = direction in RIGHT_CMD
        if any((forward, left, right)):
            for _ in range(multiple):
                self.position += self.heading * forward
                if left:
                    self.heading = self.heading.left()
                elif right:
                    self.heading = self.heading.right()
                new = self.position not in self.visited
                if not peek:
                    self.log()
            if peek:
                position = self.position
                heading = self.heading
                self.position, self.heading = self.history[-1]
                return position, heading, new
            else:
                return self.position, self.heading, new
        else:
            position, new = self.move(direction, multiple, peek)
            return position, self.heading, new

    def move(self, direction, multiple=1, peek=False):
        if multiple < 1:
            return self.position, False
        assert direction in self.names or isinstance(direction, Point), 'unknown command!'
        if not isinstance(direction, Point):
            direction = self.names[direction]
        for _ in range(multiple):
            self.position += direction
            new = self.position not in self.visited
            if not peek:
                self.log()
        if peek:
            position = self.position
            self.position, self.heading = self.history[-1]
            return position, new
        else:
            return self.position, new

    def revert(self, multiple=1):
        for _ in range(multiple):
            self.history.pop()
            self.position, self.heading = self.history[-1]

    def neighbors(self, point=None):
        if point is None:
            point = self.position
        for d in self.neighbors_list:
            yield point + d

    def goto(self, position=None, heading=None):
        if position is not None:
            self.position = position
        if heading is not None:
            self.heading = heading
        self.log()

    def log(self):
        self.visited.add(self.position)
        self.history.append((self.position, self.heading))
