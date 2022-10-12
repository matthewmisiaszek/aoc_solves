import dancer
from common.misc import md5hash


def main(input_string, verbose=False):
    pw_len = 8
    ph_char = '*'
    hstart = '00000'
    hslen = len(hstart)
    i6 = 5
    i7 = 7
    seed = input_string
    p1, p1c = [ph_char] * pw_len, 0
    p2, p2c = [ph_char] * pw_len, 0
    i = 0
    while p1c < pw_len or p2c < pw_len:
        h = md5hash(seed + str(i))
        if h[:hslen] == hstart:
            h6, h7 = h[i6:i7]
            if p1c < pw_len:
                p1[p1c] = h6
                p1c += 1
            if h6.isdigit():
                h6 = int(h6)
                if h6 < pw_len and p2[h6] == ph_char:
                    p2[h6] = h7
                    p2c += 1
        i += 1
        if verbose:
            if i % 1000 == 0:
                print('\rHacking... ' + ''.join(p1) + ' ' + ''.join(p2), end='')
    p1 = ''.join(p1)
    p2 = ''.join(p2)
    if verbose:
        print('\rHacked!:   ' + p1 + ' ' + p2)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2016, day=5, verbose=True)
