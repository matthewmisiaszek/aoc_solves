import dancer


def balance(structure, weights, bottom):
    child_weights = {}
    q = [bottom]
    while q:
        current = q.pop()
        children = structure[current]
        if children:
            todo = children - child_weights.keys()
            if todo:
                q.append(current)
                q += list(todo)
            else:
                disc = {}
                for child in children:
                    weight = child_weights[child]
                    if weight not in disc:
                        disc[weight] = set()
                    disc[weight].add(child)
                if len(disc) > 1:
                    correct_weight = max(disc.keys(), key=lambda x: len(disc[x]))
                    wrong_weight = min(disc.keys(), key=lambda x: len(disc[x]))
                    wrong_program = disc[wrong_weight].pop()
                    return weights[wrong_program] + correct_weight - wrong_weight
                else:
                    child_weights[current] = weights[current] + weight * len(children)
        else:
            child_weights[current] = weights[current]


def main(input_string, verbose=False):
    for a, b in (('(', ''), (')', ''), ('->', ''), (', ', ' ')):
        input_string = input_string.replace(a, b)
    all_children = set()
    structure = {}
    weights = {}
    for line in input_string.split('\n'):
        line = line.split()
        parent = line.pop(0)
        weight = int(line.pop(0))
        children = set(line)
        all_children.update(children)
        structure[parent] = children
        weights[parent] = weight
    p1 = (structure.keys() - all_children).pop()
    p2 = balance(structure, weights, p1)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2017, day=7, verbose=True)
