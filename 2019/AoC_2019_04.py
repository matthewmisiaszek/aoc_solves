import dancer


def main(input_string, verbose=False):
    rn, rx = (int(i) for i in input_string.split('-'))
    sgl = tuple(str(i) for i in range(10))
    dbl = tuple(i * 2 for i in sgl)
    tpl = tuple(i * 3 for i in sgl)
    dbl_tpl = tuple(zip(dbl, tpl))
    p1, p2 = 0, 0
    for pw in range(rn, rx + 1):
        pws = str(pw)
        for a, b in zip(pws, pws[1:]):
            if b < a:
                break
        else:
            p1_pass = False
            p2_pass = False
            for dbl, tpl in dbl_tpl:
                if dbl in pws:
                    p1_pass = True
                    if tpl not in pws:
                        p2_pass = True
                if p1_pass and p2_pass:
                    break
            p1 += p1_pass
            p2 += p2_pass
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2019, day=4, verbose=True)
