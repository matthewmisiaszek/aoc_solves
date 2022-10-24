import dancer


def main(input_string, verbose=False):
    p1, p2 = 0, 0
    i = input_string.find('\\')
    while i >= 0:
        if input_string[i + 1] == 'x':
            p1 += 3
        else:
            p1 += 1
        i = input_string.find('\\', i + 2)
    p1 += (input_string.count('\n') + 1) * 2
    p2 = input_string.count("\"") + input_string.count("\\") + (input_string.count('\n') + 1) * 2

    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2015, day=8, verbose=True)
