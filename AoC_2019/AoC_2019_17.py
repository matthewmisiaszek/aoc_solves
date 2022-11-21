import dancer
from AoC_2019.intcode import Intcode
from common import constants as con, elementwise as ew, cart2d
import re


def parse(ascii_str):
    scaffold = {(x, y): c
                for y, line in enumerate(ascii_str.split('\n'))
                for x, c in enumerate(line) if c != '.'}
    alignment_sum = 0
    ends = set()
    corners = set()
    intersections = set()
    for node in scaffold.keys():
        neighbor_count = 0
        neighbors = []
        for direction in con.D2D4:
            neighbor = ew.sum2d(node, direction)
            if neighbor in scaffold:
                neighbors.append(neighbor)
                neighbor_count += 1
        if neighbor_count > 2:
            alignment_sum += ew.prod(node)
            intersections.add(node)
        elif neighbor_count < 2:
            ends.add(node)
            intersections.add(node)
        else:
            (ax, ay), (bx, by) = neighbors
            if ax == bx or ay == by:
                pass
            else:
                corners.add(node)
        for end in ends:
            if scaffold[end] == '#':
                scaffold_end = end
            else:
                dock = end
    return alignment_sum, scaffold, corners, intersections, dock, scaffold_end


def find_path(scaffold, dock, scaffold_end):
    cart = cart2d.Cart()
    heading = cart.north
    loc = dock
    cmd = []
    dist = 0
    while True:
        if heading.move(loc) not in scaffold:
            cmd.append(str(dist))
            if loc == scaffold_end:
                break
            dist = 0
            if heading.right.move(loc) in scaffold:
                cmd.append('R')
                heading = heading.right
            else:
                cmd.append('L')
                heading = heading.left
        else:
            dist += 1
            loc = heading.move(loc)
    return cmd[1:]


def compress(cmd):
    pattern = r'^(.{1,21})(?:,\1)*,(.{1,21})(?:,\1|,\2)*,(.{1,21})(?:,\1|,\2|,\3)*$'
    cmdstr = ','.join(cmd)
    (a, b, c), = re.findall(pattern, cmdstr)
    mmr = cmdstr
    for i, I in ((a, 'A'), (b, 'B'), (c, 'C')):
        mmr = mmr.replace(i, I)
    cvf = 'n'
    EOM = ''
    ipf = '\n'.join((mmr, a, b, c, cvf, EOM))
    message = [ord(i) for i in ipf]
    return message


def main(input_string, verbose=False):
    program = [int(i) for i in input_string.split(',')]
    vacbot = Intcode(program)
    vacbot.prgm[0] = 2
    vacbot.run()
    ascii_str = ''.join(chr(i) for i in vacbot.output)
    scaffold_str, _ = ascii_str.split('\n\n')
    alignment_sum, scaffold, corners, intersections, dock, scaffold_end = parse(scaffold_str)
    p1 = alignment_sum
    full_path = find_path(scaffold, dock, scaffold_end)
    program = compress(full_path)
    vacbot.input.extend(program)
    p2 = vacbot.run()
    if verbose:
        ascii_str = ''.join(chr(i) for i in vacbot.output)
        print(ascii_str)

    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2019, day=17, verbose=True)
