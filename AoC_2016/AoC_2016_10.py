import blitzen
import re
from collections import defaultdict
from math import prod

@blitzen.run
def main(input_string, verbose=False):
    give_pattern = r'(.* \d+) gives low to (.* \d+) and high to (.* \d+)'
    give = {giver: (low, high) for giver, low, high in re.findall(give_pattern, input_string)}
    goes_pattern = r'value (\d+) goes to (.* \d+)'
    bots = defaultdict(list)
    comp = {}
    queue = []
    for value, recipient in re.findall(goes_pattern, input_string):
        bots[recipient].append(int(value))
        queue.append(recipient)
    while queue:
        bot = queue.pop()
        botbot = bots[bot]
        if len(botbot) == 2:
            n, x = min(botbot), max(botbot)
            givebot = give[bot]
            bots[givebot[0]].append(n)
            bots[givebot[1]].append(x)
            bots[bot] = []
            queue += givebot
            comp[(n, x)] = bot
    p1 = comp[(17, 61)].split()[1]
    p2 = prod(sum(bots['output ' + str(i)]) for i in range(3))
    return p1, p2

