import DANCER
import string

def main(input_string, verbose=False):
    alf = string.ascii_lowercase
    f = input_string.split("\n")
    check3 = 0
    check2 = 0
    for l in f:
        find3 = False
        find2 = False
        for a in alf:
            find2 = find2 or l.count(a) == 2
            find3 = find3 or l.count(a) == 3
        check3 += find3
        check2 += find2

    p1 = check2 * check3
    found = False
    l1 = -1
    while not found:
        l1 += 1
        l2 = l1
        while l2 < len(f) - 1 and not found:
            l2 += 1
            countdiff = sum([not f[l1][i] == f[l2][i] for i in range(len(f[l1]))])
            found = countdiff <= 1
    s = ''
    for i in range(len(f[l1])):
        if f[l1][i] == f[l2][i]:
            s += f[l1][i]
    p2 = s
    return p1, p2


if __name__ == "__main__":
    DANCER.run(main, year=2018, day=2, verbose=True)
