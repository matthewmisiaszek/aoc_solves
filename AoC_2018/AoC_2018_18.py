import blitzen


def main(input_string, verbose=False):
    f = input_string.split('\n')
    field = {}
    for y, line in enumerate(f):
        for x, c in enumerate(line):
            field[(x, y)] = c

    xn, yn = min(field.keys())
    xx, yx = max(field.keys())
    s = ''
    for y in range(yn, yx + 1):
        for x in range(xn, xx + 1):
            s += field[(x, y)]
        s += '\n'
    if verbose:
        print(s)
    history = []
    for minute in range(700):

        newfield = {}
        for x in range(xn, xx + 1):
            for y in range(yn, yx + 1):
                counter = 0
                current = field[(x, y)]
                if current == '|':
                    for xi in range(x - 1, x + 2):
                        for yi in range(y - 1, y + 2):
                            if (xi, yi) != (x, y):
                                if (xi, yi) in field and field[(xi, yi)] == '#':
                                    counter += 1
                    if counter >= 3:
                        newfield[(x, y)] = '#'
                    else:
                        newfield[(x, y)] = '|'
                elif current == '.':
                    for xi in range(x - 1, x + 2):
                        for yi in range(y - 1, y + 2):
                            if (xi, yi) != (x, y):
                                if (xi, yi) in field and field[(xi, yi)] == '|':
                                    counter += 1
                    if counter >= 3:
                        newfield[(x, y)] = '|'
                    else:
                        newfield[(x, y)] = '.'
                elif current == '#':
                    counter2 = 0
                    for xi in range(x - 1, x + 2):
                        for yi in range(y - 1, y + 2):
                            if (xi, yi) != (x, y):
                                if (xi, yi) in field and field[(xi, yi)] == '|':
                                    counter += 1
                                elif (xi, yi) in field and field[(xi, yi)] == '#':
                                    counter2 += 1

                    if counter >= 1 and counter2 >= 1:
                        newfield[(x, y)] = '#'
                    else:
                        newfield[(x, y)] = '.'
        field = newfield

        trees = {k: v for k, v in field.items() if v == '|'}
        yards = {k: v for k, v in field.items() if v == '#'}
        score = len(trees) * len(yards)
        history.append(score)

    # print(history)
    # print(score)
    history = history[:-1]
    x = list(reversed(history)).index(score) + 1

    # print(x)
    p2 = history[-x + (1000000000 - 1 - len(history)) % x]
    p1 = history[9]
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2018, day=18, verbose=True)
