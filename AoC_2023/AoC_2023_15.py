import dancer


def hash_alg(x):
    h = 0
    for c in x:
        h += ord(c)
        h *= 17
        h %= 256
    return h


def focusing_power(boxes):
    power = 0
    for boxi, (labels, lenses) in enumerate(boxes):
        for labeli, label in enumerate(labels):
            power += (boxi + 1) * (labeli + 1) * int(lenses[label])
    return power


def main(input_string, verbose=False):
    p1 = sum(hash_alg(step) for step in input_string.split(','))
    boxes = [([], {}) for _ in range(256)]
    for step in input_string.split(','):
        a = step[-1]
        if a == '-':
            label = step[:-1]
            op = a
        else:
            label = step[:-2]
            op = step[-2]
            lens = a
        labels, lenses = boxes[hash_alg(label)]
        if op == '-':
            if label in lenses:
                labels.remove(label)
                lenses.pop(label)
        else:
            if label not in lenses:
                labels.append(label)
            lenses[label] = lens
    p2 = focusing_power(boxes)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2023, day=15, verbose=True)
