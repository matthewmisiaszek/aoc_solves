import blitzen


def parse(input_string):
    plant = '#'
    initial_state, rules = input_string.split('\n\n')
    initial_state = initial_state[len('initial state: '):]
    pots = tuple(c is plant for c in initial_state)
    rules = tuple(line.split(' => ') for line in rules.split('\n'))
    rules = {tuple(c is plant for c in rule) for rule, res in rules if res is plant}
    return pots, rules


def generate(pots, rules):
    for rule in rules:
        break
    rule_len = len(rule)
    offset = 0
    history = []
    closed = set()
    while pots not in closed:
        closed.add(pots)
        history.append((offset, pots))
        pots = (False, )*rule_len + pots + (False, )*rule_len
        pots = tuple(pots[i:i + rule_len] in rules for i in range(len(pots) - rule_len))
        last_true = len(pots)-list(reversed(pots)).index(True)
        noffset = pots.index(True)
        pots = pots[noffset:last_true]
        offset += rule_len//2 - rule_len + noffset
    history.append((offset, pots))
    return history


def get_sum(history, generation):
    if generation<len(history):
        offset, pots = history[generation]
    else:
        idx2 = len(history)-1
        o2, p2 = history[idx2]
        offset_history, pot_history = zip(*history)
        idx1 = pot_history.index(p2)
        o1 = offset_history[idx1]
        extra_generations = generation - idx1
        repeats = extra_generations //(idx2 - idx1)
        idx3 = idx1 + extra_generations % (idx2 - idx1)
        o3, p3 = history[idx3]
        offset = o3 + (o2 - o1) * repeats
        pots = p3
    pots = [i for i, pot in enumerate(pots) if pot]
    return sum(pots)+offset*len(pots)



def main(input_string, verbose=False):
    pots, rules = parse(input_string)
    history = generate(pots, rules)
    p1 = get_sum(history, 20)
    p2 = get_sum(history, 50000000000)
    return p1,p2


if __name__ == "__main__":
    blitzen.run(main, year=2018, day=12, verbose=True)
