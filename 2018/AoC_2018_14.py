import core


def main(input_string, verbose=False):
    n_recipes = int(input_string)
    e1, e2 = 0, 1
    scoreboard = '37'
    while input_string not in scoreboard[-11:]:
        se1 = int(scoreboard[e1])
        se2 = int(scoreboard[e2])
        scoreboard += str(se1 + se2)
        sblen = len(scoreboard)
        e1 = (e1 + 1 + se1) % sblen
        e2 = (e2 + 1 + se2) % sblen
    p1 = scoreboard[n_recipes:n_recipes + 10]
    p2 = scoreboard.find(input_string)
    return p1, p2


if __name__ == "__main__":
    core.run(main, year=2018, day=14, verbose=True)
