import blitzen
from AoC_2019.intcode import Intcode
from itertools import combinations_with_replacement as combo


def check_point(drone, point):
    x, y = point
    drone.load_state()
    drone.input.extend([x, y])
    return drone.run() == 1


def main(input_string, verbose=False):
    program = [int(i) for i in input_string.split(',')]
    drone = Intcode(program)
    beam = set()
    for x, y in combo(range(50), 2):
        if check_point(drone, (x, y)):
            beam.add((x, y))
    p1 = len(beam)
    x, y = 0, 0  # top-left corner of santa's ship
    ship_size = 100  # size of santa's ship
    while True:
        x += 1
        while check_point(drone, (x + ship_size - 1, y)) is False:
            y += 1
        if check_point(drone, (x, y + ship_size - 1)) is True:
            break
    p2 = x * 10000 + y
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2019, day=19, verbose=True)
