import blitzen
import collections
import re


def main(input_string, verbose=False):
    pattern = '(.*) players; last marble is worth (.*) points'
    nplayers, nmarbles1 = (int(i) for i in re.findall(pattern, input_string)[0])
    nmarbles2 = nmarbles1 * 100

    players = [0] * nplayers
    marbles = collections.deque([0])
    for marble in range(1, nmarbles2 + 1):
        if marble % 23 == 0:
            marbles.rotate(-7)
            players[marble % len(players)] += marbles.pop() + marble
        else:
            marbles.rotate(2)
            marbles.append(marble)
        if marble == nmarbles1:
            p1 = max(players)
    p2 = max(players)
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2018, day=9, verbose=True)
