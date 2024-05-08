import blitzen


def deal_into_new(card, deck, var, rev):
    return deck - card - 1


def deal_with_increment(card, deck, var, rev=False):
    if rev is True:
        while card % var != 0:
            card += deck
        return card // var
    else:
        return (card * var) % deck


def cut(card, deck, var, rev=False):
    if rev is True:
        return (card + var) % deck
    else:
        return (card - var) % deck


def shuffle(deck, card, process, rev=False):
    for technique, var in process:
        card = technique(card, deck, var, rev)
    return card


def inv(n, deck):
    # modular inverse per Euler's theorem
    return pow(n, deck - 2, deck)


def parse(input_string):
    techniques = {'deal into new': deal_into_new,
                  'deal with increment': deal_with_increment,
                  'cut': cut}
    for technique in tuple(techniques.keys()):
        technique_nosp = technique.replace(' ', '')
        input_string = input_string.replace(technique, technique_nosp)
        techniques[technique_nosp] = techniques.pop(technique)
    process = []
    for step in input_string.split('\n'):
        technique, var = step.split()
        if var.lstrip('-').isdigit():
            var = int(var)
        process.append((techniques[technique], var))
    return process, techniques


@blitzen.run
def main(input_string, verbose=False):
    process, techniques = parse(input_string)
    p1 = shuffle(10007, 2019, process)
    process.reverse()
    deck = 119315717514047
    card = 2020
    n = 101741582076661
    a = shuffle(deck, 0, process, rev=True)
    b = shuffle(deck, 1, process, rev=True)
    offset_fact = a
    increment_mul = b - a
    # this bit is cribbed from u/mcpower_ on reddit
    increment = pow(increment_mul, n, deck)
    offset = offset_fact * (1 - increment) * inv(1 - increment_mul, deck)
    p2 = (increment * card + offset) % deck
    return p1, p2

