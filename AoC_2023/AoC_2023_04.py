import dancer


def count_matches(card):
    _, numbers = card.split(': ')
    win, have = numbers.split(' | ')
    win, have = (set(i.split()) for i in (win, have))
    return len(win & have)


def main(input_string, verbose=False):
    matches = [count_matches(line) for line in input_string.split('\n')]
    p1 = sum((2 ** (i - 1) for i in matches if i))
    copies = {i: 1 for i in range(len(matches))}
    for i in range(len(matches)):
        for j in range(i + 1, i + 1 + matches[i]):
            copies[j] += copies[i]
    p2 = sum(copies.values())
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2023, day=4, verbose=True)
