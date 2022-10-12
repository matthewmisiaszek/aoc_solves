import dancer
import re


def part1(file):
    i = file.find('(')
    while i >= 0:
        j = file.find(')', i)
        marker = file[i + 1:j]
        a, b = (int(c) for c in marker.split('x'))
        file = file[:i] + file[j + 1:j + 1 + a] * b + file[j + 1 + a:]
        i = file.find('(', i + a * b)
    return len(file)


def part2(file):
    i = file.find('(')
    if i == -1:
        return len(file)
    ret = i
    while i != -1:
        x = file.find('x', i)
        r = file.find(')', i)
        chrs = int(file[i + 1:x])
        rept = int(file[x + 1:r])
        ret += part2(file[r + 1:r + 1 + chrs]) * rept
        i = file.find('(', r + chrs)
        if i != -1:
            ret += i - (r + 1 + chrs)
    return ret


def main(input_string, verbose=False):
    file = re.sub('\n| ', '', input_string)
    p1 = part1(file)
    p2 = part2(file)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2016, day=9, verbose=True)
