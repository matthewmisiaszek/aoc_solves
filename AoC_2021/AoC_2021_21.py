import blitzen


def part2(positions, scores=(0, 0), cache=None):
    if cache is None:
        cache = {}
    dice = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}
    if (positions, scores) in cache:
        return cache[(positions, scores)]
    else:
        wins = [0, 0]
        for d in dice:
            new_positions = (positions[1], (positions[0] + d) % 10)
            new_scores = (scores[1], scores[0] + new_positions[1] + 1)
            if new_scores[1] >= 21:
                wins[0] += dice[d]
            else:
                new_wins = part2(new_positions, new_scores, cache)
                wins = [wins[i] + new_wins[1 - i] * dice[d] for i in range(2)]
        cache[(positions, scores)] = wins
        return wins


def part1(positions):
    scores, positions, roll, player = [0, 0], list(positions), 0, 0
    while max(scores) < 1000:
        for nroll in range(3):
            roll += 1
            positions[player] += roll
        positions[player] %= 10
        scores[player] += positions[player] + 1
        player = 1 - player
    return scores, roll, min(scores) * roll


@blitzen.run
def main(input_string, verbose=False):
    positions = [int(line.split()[-1]) - 1 for line in input_string.split('\n')]
    p1 = part1(positions)[-1]
    p2 = max(part2(tuple(positions)))
    return p1, p2

