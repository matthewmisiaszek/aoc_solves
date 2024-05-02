import blitzen


def combat(hands, recursive=False):
    history = set()
    while all(hands):
        if recursive:
            hands_hashable = tuple(tuple(hand) for hand in hands)
            if hands_hashable in history:
                return 0, 0
            history.add(hands_hashable)
        cards = [hand.pop(0) for hand in hands]
        if recursive and all((len(hand) >= card for card, hand in zip(cards, hands))):
            winner, _ = combat([hand[:card] for card, hand in zip(cards, hands)], recursive)
        else:
            winner = cards.index(max(cards))
        if winner == 1:
            cards = reversed(cards)
        hands[winner] += cards
    winner = 1 - hands.index([])
    score = sum(((i + 1) * card for i, card in enumerate(reversed(hands[winner]))))
    return winner, score


def main(input_string, verbose=False):
    hands = [[int(i) for i in player.split('\n') if i.isdigit()] for player in input_string.split('\n\n')]
    hands2 = [hand.copy() for hand in hands]
    p1 = combat(hands)[1]
    p2 = combat(hands2, recursive=True)[1]
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2020, day=22, verbose=True)
