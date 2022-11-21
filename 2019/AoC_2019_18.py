import dancer
from common import graph, elementwise as ew, constants as con
from string import ascii_lowercase as alph

WALL = '#'
START = '@'


def parse(input_string):
    tunnel_map = {(x, y): c
                  for y, line in enumerate(input_string.split('\n'))
                  for x, c in enumerate(line) if c != WALL}
    return tunnel_map


def four_vaults(tunnel_map, starts):
    new_starts = tuple()
    inv_map = {val: key for key, val in tunnel_map.items()}
    for start in starts:
        start_key = inv_map[start]
        tunnel_map.pop(start_key)
        for direction in con.D2D4:
            neighbor = ew.sum2d(start_key, direction)
            tunnel_map.pop(neighbor)
        for i, direction in enumerate(con.D2D8[1::2]):
            i = str(i)
            neighbor = ew.sum2d(start_key, direction)
            tunnel_map[neighbor] = i
            new_starts += (i,)
    return new_starts


def make_tunnel_graph(tunnel_map, starts):
    tunnel_graph = graph.Graph()
    for node in tunnel_map.keys():
        for direction in con.D2D4:
            neighbor = ew.sum2d(node, direction)
            if neighbor in tunnel_map:
                tunnel_graph.add_edge_eq(node, neighbor)
    doors_keys = {val: key for key, val in tunnel_map.items()}
    doors_keys.pop('.')
    keys = {val: key for key, val in doors_keys.items() if key in alph}
    starts = {val: key for key, val in doors_keys.items() if key in starts}
    keys.update(starts)
    doors = {val: key for key, val in doors_keys.items() if val not in keys}
    return tunnel_graph, keys, doors


def make_key_graph(tunnel_graph, keys, doors):
    key_graph = {}
    for loc, key in keys.items():
        key_graph[key]={}
        other_keys = keys.keys() - {loc}
        paths = tunnel_graph.dijkstra(loc, other_keys, all_paths=True, full_paths=True)
        for path in paths:
            dest = keys[path[-1]]
            if dest not in key_graph[key]:
                keys_on_path = {keys[loc] for loc in path if loc in keys}
                keys_on_path.discard(dest)
                doors_on_path = {doors[loc] for loc in path if loc in doors}
                path_len = len(path) - 1
                key_graph[key][dest] = (path_len, doors_on_path, keys_on_path)
    return key_graph


def get_the_keys(key_graph, start):
    start = tuple(sorted(start))
    q = {(0, start, start)}  # distance, visited keys, current keys
    closed = set()
    while q:
        curr = min(q)
        q.discard(curr)
        dist, visited, loc = curr
        if len(visited) == len(key_graph.keys()):
            break
        if (visited, loc) not in closed:
            closed.add((visited, loc))
            to_visit = key_graph.keys() - visited
            for current_key in loc:
                current_keys = set(loc)
                current_keys.discard(current_key)
                current_keys = tuple(current_keys)
                for next_key in to_visit & key_graph[current_key].keys():
                    path_len, doors_on_path, keys_on_path = key_graph[current_key][next_key]
                    for door in doors_on_path:
                        if door.lower() in to_visit:
                            break
                    else:
                        for key in keys_on_path:
                            if key in to_visit:
                                break
                        else:
                            new_visited = tuple(sorted(visited + (next_key,)))
                            new_current = tuple(sorted(current_keys + (next_key,)))
                            if (new_visited, new_current) not in closed:
                                q.add((dist + path_len, new_visited, new_current))
    return dist


def main(input_string, verbose=False):
    tunnel_map = parse(input_string)
    start = (START,)
    tunnel_graph, keys, doors = make_tunnel_graph(tunnel_map, start)
    key_graph = make_key_graph(tunnel_graph, keys, doors)
    p1 = get_the_keys(key_graph, start)
    start = four_vaults(tunnel_map, start)
    tunnel_graph, keys, doors = make_tunnel_graph(tunnel_map, start)
    key_graph = make_key_graph(tunnel_graph, keys, doors)
    p2 = get_the_keys(key_graph, start)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2019, day=18, verbose=True)
