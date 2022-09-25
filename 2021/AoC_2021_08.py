import core


def main(input_string, verbose=False):
    f = input_string.split('\n')
    p2 = 0
    p1 = 0
    for line in f:
        outstr = ''
        ins, outs = line.split(' | ')
        ins = ins.split()
        ins.sort(key=len)
        ones, four = [set([i for i in ins[j]]) for j in (0, 2)]
        for outi in outs.split():
            outlen = len(outi)
            easydict = {2: '1', 3: '7', 4: '4', 7: '8'}
            if outlen in easydict:
                p1 += 1
                outstr += easydict[outlen]
            elif outlen == 6:
                outi = set([i for i in outi])
                if len(outi.intersection(ones)) == 2:
                    if len(outi.intersection(four)) == 4:
                        outstr += '9'
                    else:
                        outstr += '0'
                else:
                    outstr += '6'
            elif outlen == 5:
                outi = set([i for i in outi])
                if len(outi.intersection(ones)) == 2:
                    outstr += '3'
                elif len(outi.intersection(four)) == 3:
                    outstr += '5'
                else:
                    outstr += '2'
        p2 += int(outstr)

    return p1, p2


if __name__ == "__main__":
    core.run(main, year=2021, day=8, verbose=True)
