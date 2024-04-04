import dancer


def dig(dists, heads):
    heads = heads[-1:] + heads + heads[:1]
    cw = len(heads) // 2 < sum((a + 1) % 4 == b for a, b in zip(heads, heads[1:]))
    if not cw:
        # this solution only works if the digger is going CW
        # if it's going CCW, mirror the input
        flip = {0: 2, 2: 0, 1: 1, 3: 3}
        heads = [flip[i] for i in heads]
    ypos = area = 0
    for head_prev, head, head_next, dist in zip(heads, heads[1:], heads[2:], dists):
        match head:
            case 3:
                ypos += dist
            case 1:
                ypos -= dist
            case 0:
                dist += -1 + (head_prev == 3) + (head_next == 1)
                area += (ypos + 1) * dist
            case 2:
                dist += -1 + (head_prev == 1) + (head_next == 3)
                area -= ypos * dist
    return area


def main(input_string, verbose=False):
    heads, dists, c = zip(*(line.split() for line in input_string.split('\n')))
    head_dict = {'R': 0, 'D': 1, 'L': 2, 'U': 3}
    heads = [head_dict[i] for i in heads]
    dists = [int(i) for i in dists]
    p1 = dig(dists, heads)
    dists, heads = zip(*((int(hexc[2:7], 16), int(hexc[7])) for hexc in c))
    p2 = dig(dists, heads)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2023, day=18, verbose=True)
