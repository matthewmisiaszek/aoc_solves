import blitzen
from donner import graph, spatial


WALL = '#'
SPACE = ' '
DOT = '.'
ISUFFIX = '_IN'
OSUFFIX = '_OUT'
START = 'AA'
END = 'ZZ'
BWIDTH = 3


def find_portals(donut_map, donut2D):
    bound = spatial.bounds(donut_map.keys(), pad=spatial.Point(-BWIDTH, -BWIDTH, 0))
    portal_pairs = []
    portals = {}
    for key, val in donut_map.items():
        if val != DOT:
            letter1 = val
            letter2 = None
            dot = None
            for neighbor in donut2D.graph[key].keys():
                val2 = donut_map[neighbor]
                if val2 == DOT:
                    dot = neighbor
                else:
                    letter2 = val2
            if letter2 is not None and dot is not None:
                if dot.x > key.x or dot.y > key.y:
                    pkey = ''.join([letter1, letter2])
                else:
                    pkey = ''.join([letter2, letter1])
                if spatial.inbounds(dot, bound):
                    # inside portal
                    portal_pairs.append((pkey + ISUFFIX, pkey + OSUFFIX))
                    portals[pkey + ISUFFIX] = dot
                else:
                    # outside portal
                    portals[pkey + OSUFFIX] = dot
    return portals, portal_pairs


def part1(donut1D, portal_pairs):
    p1graph = graph.Graph()
    for key, val in donut1D.graph.items():
        p1graph.graph[key] = val.copy()
    for ip, op in portal_pairs:
        p1graph.add_edge_eq(ip, op)
    return p1graph.simple_dijkstra(START+OSUFFIX, END+OSUFFIX)


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
    return p2graph.simple_dijkstra(START+OSUFFIX+'_0', END+OSUFFIX+'_0')


@blitzen.run
def main(input_string, verbose=False):
    donut_map = graph.text_to_dict(input_string, exclude={WALL, SPACE})
    donut2D = graph.set_to_graph(donut_map.keys())
    portals, portal_pairs = find_portals(donut_map, donut2D)
    donut1D = graph.poi_graph(donut2D, portals)
    p1 = part1(donut1D, portal_pairs)
    p2 = part2(donut1D, portal_pairs)
    return p1, p2

