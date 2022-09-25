import core
from common import elementwise as ew
from collections import Counter


def install_tiles(input_string, directions, translate):
    for a, b in translate:  # replace 2 character directions with 1 character substitutions
        input_string = input_string.replace(a, b)
    tiles = set()
    for instruction in input_string.split('\n'):
        tile = (0, 0)
        for key, val in directions.items():  # count instances of each direction in instruction and offset
            tile = ew.sum2d(tile, val, instruction.count(key))
        if tile in tiles:  # flip the tile (in set means black, not in set means white)
            tiles.discard(tile)
        else:
            tiles.add(tile)
    return tiles


def simulate_day(tiles, directions):
    adj_list = []  # list of tiles adjacent to every black tile in tiles including duplicates
    for tile in tiles:
        for direction in directions.values():
            adj = ew.sum2d(tile, direction)
            adj_list.append(adj)
    adj_count = Counter(adj_list)  # count occurrences of each adjacent tile
    tiles &= adj_count.keys()  # remove black tiles with no adjacent tiles
    for tile in tiles.copy():  # remove black tiles with >2 adjacent tiles
        if adj_count[tile] > 2:
            tiles.discard(tile)
    for tile in adj_count.keys() - tiles:  # add black tiles if white tile has ==2 adjacents
        if adj_count[tile] == 2:
            tiles.add(tile)

    return tiles


def main(input_string, verbose=False):
    # replace two character directions with 1 character substitute
    # optional: replace one character direction with substitute for consistency
    # convention: East is 0, other directions numbered CCW from East
    translate = (('ne', '1'), ('nw', '2'), ('sw', '4'), ('se', '5'), ('e', '0'), ('w', '3'))
    # convention: East is (1,0), Northeast is (0,1)
    directions = {'0': (1, 0), '1': (0, 1), '2': (-1, 1), '3': (-1, 0), '4': (0, -1), '5': (1, -1)}
    tiles = install_tiles(input_string, directions, translate)
    p1 = len(tiles)
    for day in range(100):
        tiles = simulate_day(tiles, directions)
    p2 = len(tiles)
    return p1, p2


if __name__ == "__main__":
    core.run(main, year=2020, day=24, verbose=True)
