import dancer


def main(input_string, verbose=False):
    input_ints = [int(i) for i in input_string.split()]
    _, p1, p2 = recfun(input_ints, 0)
    return p1, p2


def recfun(f, i):
    qchild = f[i]
    qmeta = f[i + 1]
    i += 2
    children = []
    p1sum = 0
    for j in range(qchild):
        i, p1val, p2val = recfun(f, i)
        children.append(p2val)
        p1sum += p1val
    p2sum = 0
    for j in range(qmeta):
        if qchild > 0:
            if 1 <= f[i] <= len(children):
                p2sum += children[f[i] - 1]
        else:
            p2sum += f[i]
        p1sum += f[i]
        i += 1
    return i, p1sum, p2sum


if __name__ == "__main__":
    dancer.run(main, year=2018, day=8, verbose=True)
