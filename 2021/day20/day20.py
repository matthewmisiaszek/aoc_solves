def getbounds(img):
    return tuple([min((si[i] for si in img)) for i in range(2)]), \
           tuple([max((si[i] for si in img)) for i in range(2)])


def enhance(img, setval, algo):
    bounds = getbounds(img)
    offsets = ((1, 1), (0, 1), (-1, 1), (1, 0), (0, 0), (-1, 0), (1, -1), (0, -1), (-1, -1))
    overhang = 2
    n_imgset = set()
    for x in range(bounds[0][0] - overhang, bounds[1][0] + overhang):
        for y in range(bounds[0][1] - overhang, bounds[1][1] + overhang):
            idx = sum([(((x + ox, y + oy) in img) == setval) * 2 ** p for p, (ox, oy) in enumerate(offsets)])
            if (algo[idx] != setval) == algo[0]:
                n_imgset.add((x, y))
    if algo[0]:
        setval = not setval
    return n_imgset, setval


def main(input_file='input.txt', verbose=False):
    algo_raw, img_raw = open(input_file).read().split('\n\n')
    algo, img_raw = tuple(c == '#' for c in algo_raw), img_raw.split('\n')
    img = set([(x, y) for x in range(len(img_raw[0])) for y in range(len(img_raw)) if img_raw[y][x] == '#'])
    setval = True
    for step in range(50):
        img, setval = enhance(img, setval, algo)
        if step == 1:
            p1 = len(img)
    p2 = len(img)
    if verbose:
        print('Part 1: {0[0]}\nPart 2: {0[1]}'.format([p1, p2]))
    return p1, p2


if __name__ == "__main__":
    main(verbose=True)
