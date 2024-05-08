import blitzen
import itertools
from donner import printer, spatial as sp, graph
from math import prod


class Tile:
    def __init__(self, raw):
        raw = raw.split('\n')
        self.id = int(raw.pop(0)[5:-1])  # tile ID
        self.raw = tuple(tuple(c for c in line) for line in raw)  # the rest of the tile data: content and edges
        self.neighbors = []  # tiles adjacent to this tile
        self.position = None  # location of this tile on the board
        self.child_edges = None
        self.parent_edges = None
        self.content = None
        self.reinit()

    def reinit(self):
        # recreate edges and content from raw
        # do this after the tile has been rotated or flipped and also on __init__
        # collect edges in East, North, West, and South directions.  Edges all run CCW.
        # self.parent_edges is edge:direction
        self.parent_edges = {}
        for direction in sp.ENWS:
            self.rotate_cw()
            self.parent_edges[self.raw[-1]] = direction
        # self.child edges is edge:(direction, flip).  If flip is True, the tile should be flipped.
        self.child_edges = {edge: (i, True) for edge, i in self.parent_edges.items()}
        self.child_edges.update({tuple(reversed(edge)): (i, False) for edge, i in self.parent_edges.items()})
        # self.raw minus edges
        self.content = tuple(line[1:-1] for line in self.raw[1:-1])

    def place(self, parent):
        # find donner edge between self and parent
        shared_edge = (parent.parent_edges.keys() & self.child_edges.keys()).pop()
        # which side of parent is donner with self?
        parent_side = parent.parent_edges[shared_edge]
        # which side of self is donner with parent?  Do we need to flip?
        child_side, flip = self.child_edges[shared_edge]
        # calculate self position from parent position and parent side
        self.position = parent.position + parent_side
        # how many times do we need to rotate to align self side with parent side
        rotation = (sp.ENWS.index(parent_side) - sp.ENWS.index(child_side) + 2) % 4
        for _ in range(rotation):
            self.rotate_ccw()
        if flip is True:
            if parent_side in {sp.NORTH, sp.SOUTH}:
                self.horizontal_flip()
            else:
                self.vertical_flip()
        self.reinit()  # recalculate edges and content

    def rotate_ccw(self):
        self.transpose()
        self.vertical_flip()

    def rotate_cw(self):
        self.vertical_flip()
        self.transpose()

    def transpose(self):
        self.raw = tuple(zip(*self.raw))

    def vertical_flip(self):
        self.raw = tuple(reversed(self.raw))

    def horizontal_flip(self):
        self.raw = tuple(tuple(reversed(line)) for line in self.raw)


def flip_set(points):
    return {point * sp.SOUTHWEST for point in points}


def rotate_set(points):
    return {point.left() for point in points}


def parse(input_string):
    # make tiles
    tile_list = [Tile(tile) for tile in input_string.split('\n\n')]
    # find neighbors
    for tile1, tile2 in itertools.combinations(tile_list, 2):
        if tile1.child_edges.keys() & tile2.child_edges.keys():
            tile1.neighbors.append(tile2)
            tile2.neighbors.append(tile1)
    return tile_list


def place_tiles(tile_list):
    # pick a tile to start with
    # enqueue
    # place that tile's neighbors and enqueue them
    seed = tile_list[0]
    seed.position = sp.Point()
    queue = [seed]
    while queue:
        tile = queue.pop()
        for neighbor in tile.neighbors:
            if neighbor.position is None:
                neighbor.place(tile)
                queue.append(neighbor)


def stitch_image(tile_list):
    # return a set of all points from all tiles
    tile_width = len(tile_list[0].content[0])
    tile_height = len(tile_list[0].content)
    marker = '#'
    points = set()
    for tile in tile_list:
        if tile.position is None:
            continue
        tx, ty = tile.position.x, tile.position.y
        for cy, line in enumerate(tile.content):
            for cx, c in enumerate(line):
                if c == marker:
                    points.add(sp.Point(tx * tile_width + cx, ty * tile_height + cy))
    return points


def get_monster(monster_file):
    # return a set of points representing the sea monster with one of the points at (0,0)
    smtxt = open(monster_file).read()
    monster = graph.text_to_dict(smtxt, include='#')
    for monster_origin in monster:  # pick a point at random and call that the origin
        break
    return {point - monster_origin for point in monster}  # locate the rest of the points from that point


def find_monsters(image, monster_pattern):
    # check for monsters in the image
    # create a monster instance at each point in the image where that point is the origin (0,0) of the monster
    # if no monsters found, flip / rotate the image until you find monsters
    # return a set of points representing all monsters
    monsters = set()
    for _ in range(2):
        for _ in range(4):
            for image_point in image:
                monster_instance = {image_point + monster_point for monster_point in monster_pattern}
                if monster_instance & image == monster_instance:
                    monsters.update(monster_instance)
            if monsters:
                return image, monsters
            image = rotate_set(image)
        image = flip_set(image)


@blitzen.run
def main(input_string, verbose=False):
    tile_list = parse(input_string)
    p1 = prod((tile.id for tile in tile_list if len(tile.neighbors) <= 2))
    place_tiles(tile_list)
    image = stitch_image(tile_list)
    monster = get_monster(blitzen.root_path+'/AoC_2020/sea_monster.txt')
    image, monsters = find_monsters(image, monster)
    p2 = len(image) - len(monsters)
    if verbose:
        print_dict = {point: 'O' if point in monsters else '~' for point in monsters | image}
        printer.printdict(print_dict, default=' ')
    return p1, p2

