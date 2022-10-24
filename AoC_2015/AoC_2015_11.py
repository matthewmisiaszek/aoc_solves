import dancer
from string import ascii_lowercase


def next_letter(letter, alph):
    return alph[alph.find(letter) + 1]


def increment(pw, alph):
    for i in range(1, len(pw) + 1):
        if pw[-i] != 'z':
            break
    else:
        return 'a' * i
    return pw[:-i] + next_letter(pw[-i], alph) + 'a' * (i - 1)


def check(pw, straights, pairs):
    for straight in straights:
        if straight in pw:
            break
    else:
        return False
    return sum(pw.count(pair) for pair in pairs) >= 2


def main(input_string, verbose=False):
    pw = input_string
    alph = ascii_lowercase
    pw = increment(pw, alph)  # first password after current
    straights = {alph[i:i + 3] for i in range(len(alph) - 2)}  # straights of 3 letters
    blacklist = {'i', 'o', 'l'}

    # get first pw with no blacklist
    minbl = [pw.find(bl) for bl in blacklist if bl in pw]
    if minbl:
        minbl = min(minbl)
        pw = pw[:minbl] + next_letter(pw[minbl], alph) + 'a' * (len(pw) - minbl - 1)

    # remove blacklist from alph
    for c in blacklist:
        alph = alph.replace(c, '')

    straights &= {alph[i:i + 3] for i in range(len(alph) - 2)}  # remove straights containing blacklist
    pairs = {a + a for a in alph}  # double letters (no blacklist)

    # check for straights and doubles already in password
    for test in pairs | straights:
        if test in pw[:-3]:
            break
    else:
        # if there's none then the nearest acceptable password will be head plus the next aabcc
        # aabcc is the shortest pattern to contain two doubles and one straight
        aabcc = [a + a + b + c + c for a, b, c in zip(alph, alph[1:], alph[2:])]
        tail = pw[-5:]
        head = pw[:-5]
        future_pw = [head + straight for straight in aabcc if straight > tail]
        if len(future_pw) < 2:
            future_pw.append(head[:-1] + next_letter(head[-1], alph) + aabcc[0])
        p1 = future_pw[0]
        p2 = future_pw[1]
        return p1, p2

    # otherwise, just check sequentially
    while check(pw, straights, pairs) is False:
        pw = increment(pw, alph)
    p1 = pw
    pw = increment(pw, alph)
    while check(pw, straights, pairs) is False:
        pw = increment(pw, alph)
    p2 = pw
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2015, day=11, verbose=True)
