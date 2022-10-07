import dancer


def main(input_string, verbose=False):
    connections = {}
    for line in input_string.split('\n'):
        parent, children = line.split(' <-> ')
        connections[parent] = children.split(', ')
    groups = {}
    while connections:
        program = min(connections.keys())
        members = {program}
        queue = connections.pop(program)
        while queue:
            current = queue.pop()
            if current not in members:
                members.add(current)
                queue += connections.pop(current)
        groups[program] = members

    p1 = len(groups['0'])
    p2 = len(groups)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2017, day=12, verbose=True)
