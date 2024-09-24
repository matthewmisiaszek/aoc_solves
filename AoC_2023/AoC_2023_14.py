import blitzen
from donner import graph, spatial, printer


ROUND = 'O'
SQUARE = '#'
SPACE = '.'
ONE_BILLION = 1000000000


def tilt(round_stones, square_domains, direction):
    for domaint, domains in square_domains[direction].items():
        n = len(round_stones & domains)
        round_stones.difference_update(domaint[n:])
        round_stones.update(domaint[:n])


def get_load(round_stones, bounds):
    return sum(bounds[1].y - stone.y + 1 for stone in round_stones)


def parse(input_string):
    platform = graph.text_to_dict(input_string)
    bounds = spatial.bounds(platform)
    round_stones = {stone for stone, shape in platform.items() if shape is ROUND}
    square_stones = {stone for stone, shape in platform.items() if shape is SQUARE}
    blanket = {p + d for p in platform for d in spatial.ENWS}
    square_stones.update(blanket - platform.keys())
    return round_stones, square_stones, bounds


def get_square_domains(square_stones, bounds):
    square_domains = {d: {} for d in spatial.ENWS}
    for direction in spatial.ENWS:
        for stone in square_stones:
            domain = []
            while True:
                stone -= direction
                if stone in square_stones or not spatial.inbounds(stone, bounds):
                    break
                domain.append(stone)
            if domain:
                square_domains[direction][tuple(domain)] = set(domain)
    return square_domains


@blitzen.run
def main(input_string, verbose=False):
    round_stones, square_stones, bounds = parse(input_string)
    square_domains = get_square_domains(square_stones, bounds)
    tilt(round_stones, square_domains, spatial.NORTH)
    p1 = get_load(round_stones, bounds)
    history, repeat = [], {}
    for cycle in range(ONE_BILLION):
        for direction in (spatial.NORTH, spatial.WEST, spatial.SOUTH, spatial.EAST):
            tilt(round_stones, square_domains, direction)
        hkey = printer.strset(round_stones)
        history.append(get_load(round_stones, bounds))
        if hkey in repeat:
            break
        repeat[hkey] = cycle
    b = repeat[hkey]
    p2 = history[(ONE_BILLION - b - 1) % (cycle - b) + b]
    return p1, p2

