import dancer

ABC = 'ABC'
XYZ = 'XYZ'


def part1(guide):
    score = 0
    for line in guide.split('\n'):
        a, b = line.split()
        opp = ABC.find(a)
        you = XYZ.find(b)
        score += you + 1
        if opp == you:  # draw
            score += 3
        elif (you - opp) % 3 == 1:  # win
            score += 6
    return score


def part2(guide):
    score = 0
    for line in guide.split('\n'):
        a, b = line.split()
        opp = ABC.find(a)
        outcome = XYZ.find(b)
        match outcome:
            case 0:  # lose
                score += 0
                score += (opp - 1) % 3 + 1
            case 1:  # draw
                score += 3
                score += opp + 1
            case 2:  # win
                score += 6
                score += (opp + 1) % 3 + 1
    return score


def main(input_string, verbose=False):
    p1 = part1(input_string)
    p2 = part2(input_string)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2022, day=2, verbose=True)
