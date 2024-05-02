import blitzen


CARDS = 'j23456789TJQKA'
JOKER = 'j'


def score(input_string):
    detailed_cards = []
    for line in input_string.split('\n'):
        card, bid = line.split()
        card_nj = card.replace(JOKER, '')
        counts_nj = tuple(card_nj.count(i) for i in card_nj)
        j_rep = card_nj[counts_nj.index(max(counts_nj))] if counts_nj else JOKER
        card_rep = card.replace(JOKER, j_rep)
        counts = tuple(sorted((card_rep.count(i) for i in card_rep), reverse=True))
        strengths = tuple(CARDS.index(i) for i in card)
        detailed_cards.append((counts, strengths, card, bid))
    detailed_cards.sort()
    return sum((int(bd) * (i + 1) for i, (co, st, ca, bd) in enumerate(detailed_cards)))


def main(input_string, verbose=False):
    p1 = score(input_string)
    input_string = input_string.replace(JOKER.upper(), JOKER)
    p2 = score(input_string)
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2023, day=7, verbose=True)
