import dancer


def count(file, opn, cls, sep, ignore=None):
    if ignore is None:
        ignore = set()
    istart = file.find(opn)
    while istart >= 0:
        depth = 0
        for iend, c in enumerate(file[istart:]):
            if c == cls:
                depth -= 1
            elif c == opn:
                depth += 1
            if depth == 0:
                break
        iend += istart
        head = file[:istart]
        mid = file[istart + 1:iend]
        tail = file[iend + 1:]
        mid = str(count(mid, opn, cls, sep, ignore))
        file = head + mid + tail
        istart = file.find(opn)
    to_count = []
    for obj in file.split(','):
        if sep in obj:
            key, val = obj.split(sep)
            if val in ignore:
                return 0
            else:
                to_count += [key, val]
        else:
            to_count.append(obj)
    return sum(int(obj) for obj in to_count if obj.lstrip('-').isdigit())


def main(input_string, verbose=False):
    file = input_string
    table = file.maketrans('[{]}', '[[]]')
    file = file.translate(table)
    p1 = count(file, '[', ']', ':')
    p2 = count(file, '[', ']', ':', {'"red"'})
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2015, day=12, verbose=True)
