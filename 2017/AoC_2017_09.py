import dancer


def main(input_string, verbose=False):
    f = input_string
    removed = 0
    garbage_start = f.find('<')
    while garbage_start != -1:
        garbage_end = garbage_start
        while f[garbage_end] != '>':
            if f[garbage_end] == '!':
                garbage_end += 2
            else:
                garbage_end += 1
                removed += 1
        f = f[:garbage_start] + f[garbage_end + 1:]
        removed += -1
        garbage_start = f.find('<')
    score = 0
    totscore = 0
    for i in range(len(f)):
        if f[i] == '{':
            score += 1
            totscore += score
        if f[i] == '}':
            score += -1
    p1 = totscore
    p2 = removed
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2017, day=9, verbose=True)

