import dancer
from common import graph, spatial as sp

WALL = '#'
headings = {v: h for v, h in zip('>^<v', sp.ENWS)}
hinv = {h: v for v, h in headings.items()}


def navigate(start, end, blizzards, non_wall, pacman):
    time = 0
    positions = {start}
    while end not in positions:
        for position in tuple(positions):
            for direction in sp.ENWS:
                positions.add(position + direction)
        new_blizzards = []
        for loc, heading in blizzards:
            loc += heading
            if (loc, heading) in pacman:
                loc = pacman[(loc, heading)]
            new_blizzards.append((loc, heading))
        blizzards = new_blizzards
        blizzard_positions = {loc for loc, heading in blizzards}
        positions -= blizzard_positions
        positions &= non_wall
        time += 1
    return time, blizzards


def cobe(non_wall):
    pacman = {}
    bn, bx = sp.bounds(non_wall, pad=1)
    for dir_1, dir_2 in ((sp.EAST, sp.SOUTH), (sp.SOUTH, sp.EAST)):
        line_head = bn
        while sp.inbounds(line_head, (bn, bx)):
            loc = line_head
            a, b = None, None
            while sp.inbounds(loc, (bn, bx)):
                if loc in non_wall and a is None:
                    a = loc - dir_2
                    b = loc
                if loc not in non_wall and a is not None:
                    pacman[(loc, dir_2)] = b
                    pacman[(a, dir_2 * -1)] = loc - dir_2
                    a, b = None, None
                loc += dir_2
            line_head += dir_1
    return pacman


def main(input_string, verbose=False):
    valley_map = graph.text_to_dict(input_string, ' ')
    walls = {key for key, val in valley_map.items() if val is WALL}
    non_wall = set(valley_map.keys()) - walls
    pacman = cobe(non_wall)
    blizzards = [(loc, headings[v]) for loc, v in valley_map.items() if v in headings]
    start, end = min(non_wall), max(non_wall)
    t1, blizzards = navigate(start, end, blizzards, non_wall, pacman)
    t2, blizzards = navigate(end, start, blizzards, non_wall, pacman)
    t3, blizzards = navigate(start, end, blizzards, non_wall, pacman)
    p1 = t1
    p2 = t1 + t2 + t3
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2022, day=24, verbose=True)
