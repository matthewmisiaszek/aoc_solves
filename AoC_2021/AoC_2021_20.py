import blitzen


@blitzen.run
def main(input_string, verbose=False):
    algo_raw, img_raw = input_string.split('\n\n')
    algo_dict = {tuple(i == '1' for i in format(idx, '09b')): c == '#'
                 for idx, c in enumerate(algo_raw.replace('\n', ''))}
    flipflop = algo_raw[0] == '#'
    img = tuple(tuple(c == '#' for c in line) for line in img_raw.split('\n'))
    height, width = len(img), len(img[0])
    default, pcount = False, []
    for step in range(50):
        vpad, hpad = ((default,) * (width + 2 * 2),) * 2, (default,) * 2
        img = vpad + tuple(hpad + imgi + hpad for imgi in img) + vpad
        width += 4
        height += 4
        img = sum(img, ())
        img = tuple(algo_dict[i]
                    for i in zip(img, img[1:], img[2:],
                                 img[width:], img[width + 1:], img[width + 2:],
                                 img[2 * width:], img[2 * width + 1:], img[2 * width + 2:]))
        if flipflop is True:
            default = not default
        width -= 2
        height -= 2
        img = tuple(img[i * (width + 2):(i + 1) * (width + 2) - 2] for i in range(height))
        if step in {1, 49}:
            pcount.append(sum([line.count(True) for line in img]))
    p1, p2 = pcount
    return p1, p2

