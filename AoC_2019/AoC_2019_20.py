import dancer
from common import constants as con, elementwise as ew, graph

STRIP = False
WALL = '#'
SPACE = ' '
DOT = '.'
ISUFFIX = '_IN'
OSUFFIX = '_OUT'
START = 'AA'
END = 'ZZ'


def find_portals(donut_map):
    xn, yn = [min((si[i] for si in donut_map.keys())) + 3 for i in range(2)]
    xx, yx = [max((si[i] for si in donut_map.keys())) - 3 for i in range(2)]
    portal_pairs = []
    portals = {}
    for key, val in donut_map.items():
        if val != DOT:
            letter1 = val
            letter2 = None
            dot = None
            for direction in con.D2D4:
                neighbor = ew.sum2d(key, direction)
                if neighbor in donut_map:
                    val2 = donut_map[neighbor]
                    if val2 == DOT:
                        dot = neighbor
                    else:
                        letter2 = val2
            if letter2 is not None and dot is not None:
                if dot[0] > key[0] or dot[1] > key[1]:
                    pkey = ''.join([letter1, letter2])
                else:
                    pkey = ''.join([letter2, letter1])
                x, y = dot
                if xn <= x <= xx and yn <= y <= yx:
                    # inside portal
                    portal_pairs.append((pkey + ISUFFIX, pkey + OSUFFIX))
                    portals[pkey + ISUFFIX] = dot
                else:
                    # outside portal
                    portals[pkey + OSUFFIX] = dot
    return portals, portal_pairs


def make_2D_graph(donut_map):
    donut2D = graph.Graph()
    for node, val in donut_map.items():
        if val is DOT:
            for direction in con.D2D4:
                neighbor = ew.sum2d(node, direction)
                if neighbor in donut_map and donut_map[neighbor] is DOT:
                    donut2D.add_edge_eq(node, neighbor)
    return donut2D


def make_1D_graph(donut2D, portals):
    inv_portals = {val: key for key, val in portals.items()}
    donut1D = graph.Graph()
    for key, val in portals.items():
        for key2, dist in donut2D.dijkstra(val, portals.values(), all_paths=True).items():
            donut1D.add_edge_eq(key, inv_portals[key2], dist)
    return donut1D


def part1(donut1D, portal_pairs):
    p1graph = graph.Graph()
    for key, val in donut1D.graph.items():
        p1graph.graph[key] = val.copy()
    for ip, op in portal_pairs:
        p1graph.add_edge_eq(ip, op)
    return p1graph.dijkstra(START+OSUFFIX, {END+OSUFFIX})[END+OSUFFIX]


def part2(donut1D, portal_pairs):
    p2graph = graph.Graph()
    for layer in range(len(donut1D.graph)):
        suffix = '_' + str(layer)
        suffix2 = '_' + str(layer + 1)
        for key, val in donut1D.graph.items():
            for key2, val2 in val.items():
                p2graph.add_edge_eq(key + suffix, key2 + suffix, val2)
        for key, val in portal_pairs:
            p2graph.add_edge_eq(key + suffix, val + suffix2)
    return p2graph.dijkstra(START+OSUFFIX+'_0', {END+OSUFFIX+'_0'})[END+OSUFFIX+'_0']


def main(input_string, verbose=False):
    donut_map = {(x, y): c
                 for y, line in enumerate(input_string.split('\n'))
                 for x, c in enumerate(line)
                 if c != WALL and c != SPACE}
    portals, portal_pairs = find_portals(donut_map)
    donut2D = make_2D_graph(donut_map)
    donut1D = make_1D_graph(donut2D, portals)
    p1 = part1(donut1D, portal_pairs)
    p2 = part2(donut1D, portal_pairs)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2019, day=20, verbose=True, strip=STRIP)
