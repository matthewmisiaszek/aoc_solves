import blitzen
import string


def reduce(f):
    len0 = 0
    while len(f) != len0:
        len0 = len(f)
        for a in string.ascii_lowercase:
            f = f.replace(a + a.upper(), '').replace(a.upper() + a, '')
    return len(f)


@blitzen.run
def main(input_string, verbose=False):
    p1 = reduce(input_string)
    p2 = min([reduce(input_string.replace(a, '').replace(a.upper(), '')) for a in string.ascii_lowercase])
    return p1, p2

