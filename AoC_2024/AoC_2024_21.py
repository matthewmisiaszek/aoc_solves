import blitzen
from donner import spatial as sp, graph, bfsqueue


KEYPAD = """
789
456
123
.0A"""

DPAD = """
.^A
<v>
"""


class Bot:
    def __init__(self, keypad, parent, name):
        self.name = name
        self.keypad = keypad
        self.ki = {v: k for k, v in self.keypad.items()}
        self.parent = parent
        self.cache = {}

    def cost(self, line):
        total_cost = 0
        for a, b in zip('A' + line, line):
            if (a, b) in self.cache:
                total_cost += self.cache[(a, b)]
                continue
            pos = self.ki[a]
            target = self.ki[b]
            path = ''
            q = bfsqueue.BFSQ({(pos, path): 1})
            for (pos, path), weight in q:
                if pos == target:
                    self.cache[(a, b)] = weight
                    total_cost += weight
                    break
                if pos not in self.keypad:
                    continue
                for c in '><^v':
                    npos = pos + sp.NAMES_2D[c]
                    if npos not in self.keypad:
                        continue
                    npath = path + c
                    q.add((npos, npath), self.parent.cost(npath + 'A'))
        return total_cost


class You:
    def __init__(self):
        pass

    def cost(self, line):
        return len(line)


def botchain(n, input_string):
    ret = 0
    key = graph.text_to_dict(KEYPAD, exclude='.')
    dpad = graph.text_to_dict(DPAD, exclude='.')
    bots = [You()]
    for _ in range(n):
        bots.append(Bot(dpad, bots[-1], 'name'))
    lastbot = Bot(key, bots[-1], 'last')
    for line in input_string.split('\n'):
        ret += lastbot.cost(line) * int(line[:-1])
    return ret


@blitzen.run
def main(input_string, verbose=False):
    p1 = botchain(2, input_string)
    p2 = botchain(25, input_string)
    return p1, p2
