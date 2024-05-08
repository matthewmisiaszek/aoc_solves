import blitzen
from donner import spatial as sp, graph


def p1neighbors(all_seats):
    return {seat: {seat + neighbor for neighbor in sp.ENWS8} & all_seats for seat in all_seats}


def p2neighbors(all_seats):
    ret = {}
    bounds = sp.bounds(all_seats)
    for seat in all_seats:
        seat_neighbors = set()
        for direction in sp.ENWS8:
            neighbor = seat + direction
            while neighbor not in all_seats:
                neighbor += direction
                if not sp.inbounds(neighbor, bounds):
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


@blitzen.run
def main(input_string, verbose=False):
    empty_seat = 'L'
    all_seats = set(graph.text_to_dict(input_string, include=empty_seat).keys())
    p1 = simulate(all_seats, p1neighbors, 4)
    p2 = simulate(all_seats, p2neighbors, 5)
    return p1, p2

