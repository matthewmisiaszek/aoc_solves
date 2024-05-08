import blitzen


def knot(lengths):
    circle_len = 256
    circle = tuple(range(circle_len))
    skip = 0
    position = 0
    for length in lengths:
        circle = circle[length:] + tuple(reversed(circle[:length]))
        circle = circle[skip:] + circle[:skip]
        position -= skip + length
        position %= circle_len
        skip += 1
        skip %= circle_len
    circle = circle[position:] + circle[:position]

    return circle


def xor(block):
    ret = block[0]
    for i in block[1:]:
        ret = ret ^ i
    return ret


def knothash(input_string):
    lengths = tuple(ord(c) for c in input_string) + (17, 31, 73, 47, 23)
    lengths *= 64
    circle = knot(lengths)
    dense_hash = [xor(circle[i:i + 16]) for i in range(0, len(circle), 16)]
    return ''.join('{:02x}'.format(a) for a in dense_hash)

@blitzen.run
def main(input_string, verbose=False):
    lengths = tuple(int(i) for i in input_string.split(','))
    circle = knot(lengths)
    p1 = circle[0] * circle[1]
    p2 = knothash(input_string)
    return p1, p2

