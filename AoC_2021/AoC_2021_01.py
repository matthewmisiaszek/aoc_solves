import blitzen


@blitzen.run
def main(input_string, verbose=False):
    f = input_string.split('\n')
    p1, p2 = (sum([int(f[i]) < int(f[i + s]) for i in range(len(f) - s)]) for s in [1, 3])
    return p1, p2

