import blitzen


@blitzen.run
def main(input_string, verbose=False):
    left, right = (sorted(k) for k in zip(*((int(j) for j in i.split()) for i in input_string.split('\n'))))
    p1 = sum(abs(l - r) for l, r in zip(left, right))
    p2 = sum(l * right.count(l) for l in left)
    return p1, p2
