import dancer


def empty(a, b):
    return b


def band(a, b):
    return a & b


def lshift(a, b):
    return a << b


def bor(a, b):
    return a ^ b


def rshift(a, b):
    return a >> b


def bnot(a, b):
    return ~b


def circuit(input_string, initial_state=None):
    wires = {'': 0}
    children = {}
    queue = set()
    for line in input_string.split('\n'):
        line = line.split(' ')
        a, op = '', ''
        if len(line) == 5:
            a, op, b, _, c = line
        elif len(line) == 4:
            op, b, _, c = line
        elif len(line) == 3:
            b, _, c = line
        for i in (a, b):
            if not i.lstrip('-').isdigit():
                if i not in children:
                    children[i] = set()
                children[i].add((a, op, b, c))
            else:
                wires[i] = int(i)
                queue.add((a, op, b, c))
    if initial_state is not None:
        wires.update(initial_state)
    ops = {'': empty, 'AND': band, 'OR': bor, 'LSHIFT': lshift, 'RSHIFT': rshift, 'NOT': bnot}
    while queue:
        a, op, b, c = queue.pop()
        if a in wires and b in wires and c not in wires:
            a = wires[a]
            b = wires[b]
            wires[c] = ops[op](a, b)
            if c in children:
                queue.update(children[c])
    return wires


def main(input_string, verbose=False):
    p1 = circuit(input_string)['a']
    p2 = circuit(input_string, {'b': p1})['a']
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2015, day=7, verbose=True)
