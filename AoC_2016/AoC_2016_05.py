import dancer
from common.misc import md5hash
from common import multiproc


START_MATCH = '00000'
START_MATCH_L = len(START_MATCH)
PWLEN = 8
FIVE = 5
SEVEN = 7
PH_CHAR = '*'


def hash_filter(start, n, seed):
    hashes = tuple(md5hash(seed + str(i)) for i in range(start, start+n))
    h57 = tuple(h[FIVE:SEVEN] for h in hashes if h[:START_MATCH_L] == START_MATCH)
    return h57


def pw_fill(mpc, result, p1, p2, pc, verbose):
    for h6, h7 in result:
        if pc[0] < PWLEN:
            p1[pc[0]] = h6
            pc[0] += 1
        if h6.isdigit():
            h6 = int(h6)
            if h6 < PWLEN and p2[h6] == PH_CHAR:
                p2[h6] = h7
                pc[1] += 1
    if pc[0] == PWLEN and pc[1] == PWLEN:
        mpc.keep_popping = False
    if verbose:
        print('\rHacking... ' + ''.join(p1) + ' ' + ''.join(p2), end='')


def main(input_string, verbose=False):
    seed = input_string
    p1, p1c = [PH_CHAR] * PWLEN, 0
    p2, p2c = [PH_CHAR] * PWLEN, 0
    pc = [0, 0]
    multiproc.pool(proc_fun=hash_filter, proc_args=(seed,),
                   post_fun=pw_fill, post_args=(p1, p2, pc, verbose))
    p1 = ''.join(p1)
    p2 = ''.join(p2)
    if verbose:
        print('\rHacked!:   ' + p1 + ' ' + p2)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2016, day=5, verbose=True)
