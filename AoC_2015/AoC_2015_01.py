import dancer


def main(input_string, verbose=False):
    p1 = input_string.count('(')-input_string.count(')')
    floor = 0
    for i, c in enumerate(input_string):
        if c == '(':
            floor += 1
        else:
            floor -= 1
        if floor == -1:
            p2 = i + 1
            break
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2015, day=1, verbose=True)
