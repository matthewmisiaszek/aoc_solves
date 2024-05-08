import blitzen
from donner import spatial as sp
from collections import Counter


def install_tiles(input_string):
    for i in 'ew':
        input_string = input_string.replace(i, i + ' ')
    tiles = set()
    for instruction in input_string.split('\n'):
        instruction = ' ' + instruction
        tile = sp.Point()
        for key, val in sp.NAMES_HEX_E.items():  # count instances of each direction in instruction and offset
            tile += val * instruction.count(' ' + key)
        if tile in tiles:  # flip the tile (in set means black, not in set means white)
            tiles.discard(tile)
        else:
            tiles.add(tile)
    return tiles


def simulate_day(tiles):
    adj_list = []  # list of tiles adjacent to every black tile in tiles including duplicates
    for tile in tiles:
        for direction in sp.HEX_E_6:
            adj = tile + direction
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


@blitzen.run
def main(input_string, verbose=False):
    tiles = install_tiles(input_string)
    p1 = len(tiles)
    for day in range(100):
        tiles = simulate_day(tiles)
    p2 = len(tiles)
    return p1, p2

