import DANCER
from common.constants import D2D8 as neighbors
from common.elementwise import esum


def p1neighbors(all_seats):
    return {seat: {esum(seat, neighbor) for neighbor in neighbors} & all_seats for seat in all_seats}


def p2neighbors(all_seats):
    ret = {}
    xn, yn = min(all_seats)
    xx, yx = max(all_seats)
    for seat in all_seats:
        seat_neighbors = set()
        for direction in neighbors:
            neighbor = esum(seat, direction)
            while neighbor not in all_seats:
                neighbor = esum(neighbor, direction)
                if not (xn <= neighbor[0] <= xx and yn <= neighbor[1] <= yx):
                    break
            else:
                seat_neighbors.add(neighbor)
        ret[seat] = seat_neighbors
    return ret


def simulate(all_seats, neighbor_fun, tolerance):
    seat_neighbors = neighbor_fun(all_seats)
    occupied_seats = set()
    new_occupied, new_empty = True, True
    while new_occupied or new_empty:
        empty_seats = all_seats - occupied_seats
        new_occupied = {seat for seat in empty_seats
                        if not seat_neighbors[seat] & occupied_seats}
        new_empty = {seat for seat in occupied_seats
                     if len(seat_neighbors[seat] & occupied_seats) >= tolerance}
        occupied_seats = (occupied_seats | new_occupied) - new_empty
    return len(occupied_seats)


def main(input_string, verbose=False):
    empty_seat = 'L'
    all_seats = {(x, y)
                 for y, line in enumerate(input_string.split('\n'))
                 for x, c in enumerate(line)
                 if c is empty_seat}
    p1 = simulate(all_seats, p1neighbors, 4)
    p2 = simulate(all_seats, p2neighbors, 5)
    return p1, p2


if __name__ == "__main__":
    DANCER.run(main, year=2020, day=11, verbose=True)
