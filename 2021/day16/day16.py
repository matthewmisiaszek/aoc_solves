def process(s, n=1):
    sumversion, cn, i, packetlist = 0, 0, 0, []
    while cn < n and i < len(s):
        sumversion += int(s[i:i + 3], 2)
        i += 3
        cn += 1
        id1 = int(s[i:i + 3], 2)
        i += 3
        if id1 == 4:  # literal value
            pstr = ''
            while s[i] == '1':
                pstr += s[i + 1:i + 5]
                i += 5
            pstr += s[i + 1:i + 5]
            packetlist.append(int(pstr, 2))
            i += 5
        else:  # operator
            id2 = s[i]
            i += 1
            if id2 == '0':
                l = int(s[i:i + 15], 2)
                i += 15
                inci, incsumversion, operlist = process(s[i:i + l], len(s))
                i += inci
                sumversion += incsumversion
            else:
                nn = int(s[i:i + 11], 2)
                i += 11
                inci, incsumversion, operlist = process(s[i:], nn)
                i += inci
                sumversion += incsumversion
            if id1 == 0:
                packetlist.append(sum(operlist))
            elif id1 == 1:
                produ = 1
                for li in operlist:
                    produ *= li
                packetlist.append(produ)
            elif id1 == 2:
                packetlist.append(min(operlist))
            elif id1 == 3:
                packetlist.append(max(operlist))
            elif id1 == 5:
                packetlist.append(operlist[0] > operlist[1])
            elif id1 == 6:
                packetlist.append(operlist[0] < operlist[1])
            elif id1 == 7:
                packetlist.append(operlist[0] == operlist[1])
    return i, sumversion, packetlist


def main(input_file='input.txt', verbose=False):
    f = open(input_file).read()
    fl = ''.join(["{0:04b}".format(int(c, 16)) for c in f])
    i, sumversion, operlist = process(fl, 1)
    p1 = sumversion
    p2 = operlist[0]

    if verbose:
        print('Part 1: {0[0]}\nPart 2: {0[1]}'.format([p1, p2]))
    return p1, p2


if __name__ == "__main__":
    main(verbose=True)
