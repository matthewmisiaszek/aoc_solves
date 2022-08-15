def main(input_file='input.txt', verbose=False):
    algo_raw, img_raw = open(input_file).read().split('\n\n')
    algo = tuple(c == '#' for c in algo_raw.replace('\n', ''))
    algo_dict = {}
    for idx, val in enumerate(algo):
        tupidx = tuple(i == '1' for i in format(idx, '09b'))
        algo_dict[tupidx] = val
    flipflop = algo[0] == True
    img = tuple(tuple(c == '#' for c in line) for line in img_raw.split('\n'))
    height, width = len(img), len(img[0])
    default, pcount = False, []
    for step in range(50):
        vpad, hpad = ((default,) * (width + 2 * 2),) * 2, (default,) * 2
        img = vpad + tuple(hpad + img[i] + hpad for i in range(height)) + vpad
        width += 4
        height += 4
        img = sum(img, ())
        img = tuple(algo_dict[i]
                    for i in zip(img,             img[1:],             img[2:],
                                 img[width:],     img[width + 1:],     img[width + 2:],
                                 img[2 * width:], img[2 * width + 1:], img[2 * width + 2:]))
        if flipflop is True:
            default = not default
        width -= 2
        height -= 2
        img = tuple(img[i * (width + 2):(i + 1) * (width + 2) - 2] for i in range(height))
        pcount.append(sum([line.count(True) for line in img]))
    p1, p2 = pcount[1], pcount[-1]
    if verbose:
        print('Part 1: {0[0]}\nPart 2: {0[1]}'.format([p1, p2]))
    return p1, p2


if __name__ == "__main__":
    main(verbose=True)
