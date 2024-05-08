import blitzen
from AoC_2017.AoC_2017_10 import knothash
from donner import misc, spatial as sp


@blitzen.run
def main(input_string, verbose=False):
    disk_size = 128
    hexstr = '0123456789abcdef'
    hex_hashes = [knothash(input_string + '-' + str(i)) for i in range(disk_size)]
    dig_hashes = [tuple(hexstr.find(c) for c in hex_hash) for hex_hash in hex_hashes]
    bit_hashes = [misc.digits(misc.digits(dig_hash, 16), 2, disk_size) for dig_hash in dig_hashes]
    used = {sp.Point(x, y) for y, line in enumerate(bit_hashes) for x, square in enumerate(line) if square}
    p1 = len(used)
    regions = 0
    while used:
        queue = [used.pop()]
        regions += 1
        while queue:
            current = queue.pop()
            for direction in sp.ENWS:
                neighbor = current + direction
                if neighbor in used:
                    used.discard(neighbor)
                    queue.append(neighbor)
    p2 = regions
    return p1, p2

