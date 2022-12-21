import dancer
import re
from common import graph
from itertools import combinations

START = 'AA'


def parse(input_string):
    # return a graph valves={valve:{other_valve: distance}} for all valves with rate > 0 plus START
    # return a dict rates={valve:rate} for all valves
    pattern = r'Valve (.*) has flow rate=(.*); tunnels? leads? to valves? ([\S ]*)'
    all_valves = graph.Graph()
    rates = {}
    for key, rate, tunnels in re.findall(pattern, input_string):
        tunnels = set(tunnels.split(', '))
        rates[key] = int(rate)
        for tunnel in tunnels:
            all_valves.add_edge_eq(key, tunnel)
    poi = {valve: valve for valve, rate in rates.items() if rate > 0}
    poi[START] = START
    valves = graph.poi_graph(all_valves, poi).graph
    return valves, rates


def best_combo(valves, closed, nworkers):
    most_pressure = 0
    pressure_opened = tuple(sorted([(pressure, set(opened)) for opened, pressure in closed.items()], reverse=True))
    all_valves = set(valves.keys())
    minp = min(closed.values())  # the minimum pressure value in the maximum pressure combo
    for c in combinations(pressure_opened, nworkers):
        p, o = zip(*c)
        if max(p) <= minp:  # no way to get a better pressure from here on
            break
        ps = sum(p)  # total pressure for this set
        if ps > most_pressure:
            if not all_valves.intersection(*o):  # check that the opened valves don't overlap
                most_pressure = ps
                minp = max(minp, min(p))
    return most_pressure


def release_pressure(valves, rates, time_limit, nworkers):
    queue = {(0, time_limit, tuple(), START)}  # pressure, time remaining, opened valves, current location
    # pressure is the pressure that will eventually be released at time=0 if no other valves are opened
    # net present value, if you will
    closed = {}  # the highest pressure recorded for a given set of valves
    while queue:
        curr = max(queue)  # take the queue item with the highest pressure
        queue.discard(curr)
        pressure, time, opened, location = curr
        if opened in closed and closed[opened] >= pressure:
            continue  # we've already found a better path to this state
        closed[opened] = pressure
        if time <= 0:
            continue
        for next_valve in valves[location].keys() - opened: # try every valve you haven't been to yet
            n_location = next_valve
            n_opened = tuple(sorted(opened + (next_valve,)))
            n_time = max(0, time - valves[location][next_valve] - 1)  # time it takes to get there plus time to open
            n_pressure = pressure + rates[next_valve] * n_time
            queue.add((n_pressure, n_time, n_opened, n_location))
    if nworkers == 1:
        return max(closed.values())
    else:
        return best_combo(valves, closed, nworkers)


def main(input_string, verbose=False):
    valves, rates = parse(input_string)
    p1 = release_pressure(valves, rates, 30, 1)
    p2 = release_pressure(valves, rates, 26, 2)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2022, day=16, verbose=True)
