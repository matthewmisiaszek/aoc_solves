import blitzen
# from donner import printer


def parse_pattern(pattern, mark, cr):
    return tuple(tuple(c == mark for c in line) for line in pattern.split(cr))


def transform(key):
    transpose = {4}
    vflip = {1, 3, 5, 7}
    hflip = {2, 6}
    yield key
    for t in range(8):
        if t in vflip:
            key = tuple(reversed(key))
            yield key
        elif t in transpose:
            key = tuple(zip(*key))
            yield key
        elif t in hflip:
            key = tuple(tuple(reversed(line)) for line in key)
            yield key


def main(input_string, verbose=False):
    p1, p2 = 5, 18
    cr = '/'
    mark = '#'
    start_pattern = '.#./..#/###'
    image = parse_pattern(start_pattern, mark, cr)
    rules = {}
    history = [0]
    for line in input_string.split('\n'):
        key, val = (parse_pattern(i, mark, cr) for i in line.split(' => '))
        for key in transform(key):
            rules[key] = val
    for iteration in range(max(p1, p2)):
        if len(image) % 2 == 0:
            size = 2
        else:
            size = 3
        chunks = {}
        nchunks = len(image) // size
        for y in range(nchunks):
            for x in range(nchunks):
                chunks[(x, y)] = rules[tuple(line[x * size:(x + 1) * size] for line in image[y * size:(y + 1) * size])]
        size += 1
        image = tuple(sum((chunks[(x, y)][r] for x in range(nchunks)), ()) for y in range(nchunks) for r in range(size))
        history.append(sum(sum(line) for line in image))
    p1 = history[p1]
    p2 = history[p2]
    # if verbose:
    #     on_set = {(x, y) for x in range(len(image)) for y in range(len(image)) if image[y][x]}
    #     printer.printset(on_set)
    #     print('')
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2017, day=21, verbose=True)
