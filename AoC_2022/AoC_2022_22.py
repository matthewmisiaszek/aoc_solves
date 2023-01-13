import dancer
from common import graph, spatial as sp
import re

# cube sides: 0: front, 1: right, 2: back, 3: left, 4: top, 5: bottom
# 4
# 0 1 2 3
# 5
# for no particular reason

WALL = '#'
FACING = (sp.EAST, sp.SOUTH, sp.WEST, sp.NORTH)
SIX = 6
FOUR = 4
TWO = FOUR // 2
# from the perspective of face N, what face is East, North, South, and West and how many times should it be rotated CCW?
cube_neighbors = {0: ((1, 0), (4, 0), (3, 0), (5, 0)),
                  1: ((2, 0), (4, 1), (0, 0), (5, 3)),
                  2: ((3, 0), (4, 2), (1, 0), (5, 2)),
                  3: ((0, 0), (4, 3), (2, 0), (5, 1)),
                  4: ((1, 3), (2, 2), (3, 1), (0, 0)),
                  5: ((1, 1), (0, 0), (3, 3), (2, 2))}


def follow_path(board, pacman, path):
    walls = {tile for tile, c in board.items() if c is WALL}
    loc = min(board.keys())
    head = sp.EAST
    for cmd in re.findall('R|L|\d+', path):
        match cmd:
            case 'R':
                head = head.right()
            case 'L':
                head = head.left()
            case _:
                for _ in range(int(cmd)):
                    loc += head
                    if (loc, head) in pacman:
                        loc, turns = pacman[(loc, head)]
                        for _ in range(turns):
                            head = head.left()
                    if loc in walls:
                        loc -= head
                        if (loc, head * -1) in pacman:
                            loc, turns = pacman[(loc, head * -1)]
                            for _ in range(turns):
                                head = head.left()

    return (loc.y + 1) * 1000 + (loc.x + 1) * 4 + FACING.index(head)


def part1(input_string):
    board, path = input_string.split('\n\n')
    board = graph.text_to_dict(board, exclude=' ')
    bn, bx = sp.bounds(board.keys(), pad=1)
    pacman = {}
    for dir_1, dir_2 in ((sp.EAST, sp.SOUTH), (sp.SOUTH, sp.EAST)):
        line_head = bn
        while sp.inbounds(line_head, (bn, bx)):
            loc = line_head
            a, b = None, None
            while sp.inbounds(loc, (bn, bx)):
                if loc in board and a is None:
                    a = loc - dir_2
                    b = loc
                if loc not in board and a is not None:
                    pacman[(loc, dir_2)] = (b, 0)
                    pacman[(a, dir_2 * -1)] = (loc - dir_2, 0)
                    a, b = None, None
                loc += dir_2
            line_head += dir_1
    return follow_path(board, pacman, path)


def part2(input_string):
    # parse input
    board, path = input_string.split('\n\n')
    board = graph.text_to_dict(board, exclude=' ')
    bn, bx = sp.bounds(board.keys(), pad=1)
    # find the six faces in the board
    face_size = int((len(board) // SIX) ** .5)  # what is the length/width of each face?  example is 4, input is 50
    n_faces_x = (bx.x - bn.x) // face_size
    n_faces_y = (bx.y - bn.y) // face_size
    present_faces = set()
    for face_x in range(n_faces_x):
        for face_y in range(n_faces_y):
            if sp.Point(face_x * face_size, face_y * face_size) in board:
                present_faces.add(sp.Point(face_x, face_y))
    # assign faces to cube
    cube = {0: (present_faces.pop(), 0)}  # where is each face of the cube located / rotated?
    queue = {0}
    while queue:
        curr = queue.pop()
        loc, turn = cube[curr]
        face_neighbors = cube_neighbors[curr]
        face_neighbors = face_neighbors[turn:] + face_neighbors[:turn]
        for (nface, nturn), d in zip(face_neighbors, sp.ENWS):
            floc = loc + d
            if floc in present_faces:
                cube[nface] = (floc, (turn + nturn) % len(face_neighbors))
                queue.add(nface)
                present_faces.discard(floc)
    # use cube to build pacman warps between edges
    pacman = {}
    headings = sp.ENWS  # the direction at which we travel off of the face
    progressions = sp.ENWS[-1:] + sp.ENWS[:-1]  # a perpendicular direction that we progress along
    corners = [sp.Point(x, y) for x, y in  # NE, NW, SW, SE corners that we start from
               ((face_size - 1, 0),
                (0, 0),
                (0, face_size - 1),
                (face_size - 1, face_size - 1))]
    for face, (loc, turn) in cube.items():  # face number, location on the board, and rotation
        face_neighbors = cube_neighbors[face]  # tuple of face number, rotation for faces East, North, West, and South
        face_origin = sp.Point(loc.x * face_size, loc.y * face_size)  # top-left corner of this face
        for i, (head, prog, corn) in enumerate(zip(headings, progressions, corners)):
            j = (i + turn) % FOUR  # j is which side of the face we're working on relative to the cube
            neighbor, nturn2 = face_neighbors[j]  # which face is the neighbor on this side and how is it rotated?
            nloc, nturn = cube[neighbor]  # what is the location of that face on the board and how is it rotated?
            nface_origin = sp.Point(nloc.x * face_size, nloc.y * face_size)
            nturn = (-nturn + nturn2 + TWO + j) % FOUR  # total rotations between faces plus 2 % 4
            ncorn = corners[nturn]  # select start corner and progression on neighbor face
            nprog = progressions[nturn]
            a = corn + face_origin + head  # starting start location on board
            b = ncorn + nface_origin + nprog * (face_size - 1)  # starting end location on board
            pturn = (nturn - i + TWO) % FOUR
            for _ in range(face_size):
                if a != b:  # don't build portals for faces that are already adjacent
                    pacman[(a, head)] = (b, pturn)
                    # {(where you landed, which way you're going):
                    # (where you should be, how many times you should turn left)}
                a += prog
                b -= nprog
    return follow_path(board, pacman, path)


def main(input_string, verbose=False):
    p1 = part1(input_string)
    p2 = part2(input_string)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2022, day=22, verbose=True)
