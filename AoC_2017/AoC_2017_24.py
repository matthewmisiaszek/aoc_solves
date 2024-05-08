import blitzen


@blitzen.run
def main(input_string, verbose=False):
    components = {tuple(int(i) for i in line.split('/')) for line in input_string.split('\n')}
    queue = {(0, tuple(), 0)}  # strength, sorted list of components, last connector
    closed = set()
    p1set = set()
    p2set = set()
    while queue:
        strength, bridge, connector = queue.pop()
        bridge_set = set(bridge)
        for component in components:
            if component not in bridge_set and connector in component:
                new_strength = strength + sum(component)
                new_bridge = tuple(sorted(bridge + (component,)))
                new_connector = sum(component) - connector
                new_item = (new_strength, new_bridge, new_connector)
                if new_item not in closed:
                    closed.add(new_item)
                    queue.add(new_item)
                    p1set.add(new_strength)
                    p2set.add((len(new_bridge), new_strength))

    p1 = max(p1set)
    _, p2 = max(p2set)
    return p1, p2

