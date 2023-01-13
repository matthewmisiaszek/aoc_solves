import dancer


DKEY = 811589153
GROVE = (1000, 2000, 3000)


def mix(file, n):
    flen = len(file)
    zind = file.index(0)
    indices = {idx: idx for idx in range(flen)}  # where it is: where it started
    indices_inv = indices.copy()  # where it started: where it is
    for _ in range(n):
        for i in range(flen):
            v = file[i]
            j = indices_inv[i]
            k = (j + v) % (flen - 1)
            if k > j:
                for m in range(j + 1, k + 1):
                    n = indices[m]
                    indices[(m - 1) % flen] = n
                    indices_inv[n] = (indices_inv[n] - 1) % flen
            else:
                for m in range(j - 1, k - 1, -1):
                    n = indices[m]
                    indices[(m + 1) % flen] = n
                    indices_inv[n] = (indices_inv[n] + 1) % flen

            indices_inv[i] = k
            indices[k] = i
    coords = []
    for x in GROVE:
        x += indices_inv[zind]
        coords.append(file[indices[x % flen]])
    return sum(coords)


def main(input_string, verbose=False):
    file = [int(i) for i in input_string.split('\n')]
    p1 = mix(file, 1)
    file = [i * DKEY for i in file]
    p2 = mix(file, 10)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2022, day=20, verbose=True)
