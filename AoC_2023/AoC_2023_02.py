import blitzen
import re
from collections import defaultdict


POSSIBLE = {
    'red': 12,
    'green': 13,
    'blue': 14,
}

PATTERN = r'(\d+) (\w+)'


@blitzen.run
def main(input_string, verbose=False):
    p1 = p2 = 0
    for game in input_string.split('\n'):
        game_id, record = game.split(': ')
        game_id = int(game_id.split(' ')[1])
        max_color = defaultdict(int)
        possible = True
        for quant, color in re.findall(PATTERN, record):
            quant = int(quant)
            max_color[color] = max(max_color[color], quant)
            if quant > POSSIBLE[color]:
                possible = False
        if possible:
            p1 += game_id
        power = 1
        for quant in max_color.values():
            power *= quant
        p2 += power
    return p1, p2

