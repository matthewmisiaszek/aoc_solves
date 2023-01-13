import dancer
from common import graph, bfsqueue, spatial

WALL = '#'
START = '@'
TUNNEL = '.'


def find_poi(tunnel_map):
    inv_map = {val: key for key, val in tunnel_map.items()}
    inv_map.pop(TUNNEL)
    doors = {val: key for key, val in inv_map.items() if key.isupper()}
    keys = {val: key for key, val in inv_map.items() if not key.isupper()}
    return keys, doors


def four_vaults(tunnel_map, starts):
    new_starts = tuple()
    inv_map = {val: key for key, val in tunnel_map.items()}
    for start in starts:
        start_key = inv_map[start]
        tunnel_map.pop(start_key)
        for direction in planar.D2D4:
            neighbor = start_key + direction
            tunnel_map.pop(neighbor)
        for i, direction in enumerate(planar.D2D8[1::2]):
            i = str(i)
            neighbor = start_key+direction
            tunnel_map[neighbor] = i
            new_starts += (i,)
    return new_starts


def make_key_graph(tunnel_graph, keys, doors):
    key_graph = {}
    for loc, key in keys.items():
        key_graph[key] = {}
        other_keys = keys.keys() - {loc}
        paths = tunnel_graph.dijkstra(loc, other_keys, all_paths=True, full_paths=True)
        for path, dist in paths.items():
            dest = keys[path[-1]]
            if dest not in key_graph[key]:
                keys_on_path = {keys[loc] for loc in path if loc in keys}
                keys_on_path.discard(dest)
                doors_on_path = {doors[loc].lower() for loc in path if loc in doors}
                key_graph[key][dest] = (dist, doors_on_path | keys_on_path)
    return key_graph


def get_the_keys(key_graph, start):
    start = tuple(sorted(start))
    to_visit = tuple(sorted(key_graph.keys() - start))
    q = bfsqueue.BFSQ((to_visit, start))  # keys to visit, current keys
    for (to_visit, current_keys), dist in q:
        if not to_visit:
            break  # no keys left to get
        to_visit = set(to_visit)
        current_keys = set(current_keys)
        for current_key in current_keys:
            for next_key in to_visit & key_graph[current_key].keys():
                path_len, on_path = key_graph[current_key][next_key]
                if not (on_path & to_visit):  # if this path is valid
                    new_to_visit = tuple(sorted(to_visit - {next_key}))
                    new_current = tuple(sorted(current_keys - {current_key} | {next_key}))
                    q.add((new_to_visit, new_current), dist + path_len)
    return dist


def main(input_string, verbose=False):
    tunnel_map = graph.text_to_dict(input_string, exclude=WALL)
    tunnel_graph = graph.set_to_graph(tunnel_map.keys())
    start = (START,)
    keys, doors = find_poi(tunnel_map)
    key_graph = make_key_graph(tunnel_graph, keys, doors)
    p1 = get_the_keys(key_graph, start)
    start = four_vaults(tunnel_map, start)
    tunnel_graph = graph.set_to_graph(tunnel_map.keys())
    keys, doors = find_poi(tunnel_map)
    key_graph = make_key_graph(tunnel_graph, keys, doors)
    p2 = get_the_keys(key_graph, start)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2019, day=18, verbose=True)
