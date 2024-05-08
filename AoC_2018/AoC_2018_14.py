import blitzen
from donner.misc import digits
from numba import njit


def main(input_string, verbose=False):
    n_recipes = int(input_string)
    return solve(n_recipes)


@njit
def solve(n_recipes):
    e1, e2 = 0, 1
    scoreboard = [3, 7]
    score_sequence = list(digits(n_recipes))
    score_len = len(score_sequence)
    while True:
        se1 = scoreboard[e1]
        se2 = scoreboard[e2]
        for i in digits(se1 + se2):
            scoreboard.append(i)
            sblen = len(scoreboard)
            if scoreboard[-score_len:] != score_sequence:
                continue
            p1 = digits(scoreboard[n_recipes:n_recipes + 10])
            p2 = sblen - score_len
            return p1, p2
        e1 = (e1 + 1 + se1) % sblen
        e2 = (e2 + 1 + se2) % sblen


if __name__ == "__main__":
    blitzen.run(main, year=2018, day=14, verbose=True)
